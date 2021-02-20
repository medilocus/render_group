#
#  Render Group
#  Blender add-on to create a local render farm.
#  Copyright Medilocus 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import os
import random
import threading
import socket
import pickle
import zlib
import bpy
from hashlib import sha256


class Client:
    header = 64
    packet_size = 8192
    padding = " " * header

    def __init__(self, ip, port, props):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))

        self.props = props
        self.status = "WAITING"
        self.frame = None

    def init(self):
        self.auth()
        if self.recv()["type"] == "get_name":
            self.send({"type": "get_name", "name": self.props.name})

        threading.Thread(target=self.start).start()

    def auth(self):
        task = self.recv()
        ans = sha256(task["task"]).hexdigest()
        self.send({"type": "auth", "answer": ans})

    def start(self):
        if self.recv()["type"] == "render_starting":
            self.status = "RENDERING"
            while True:
                info = self.recv()
                if info["type"] == "render_frame":
                    self.render(info["frame"])

    def render(self, frame):
        self.frame = frame
        bpy.context.scene.frame_set(frame)

        get_path = lambda: os.path.join(self.parent, sha256(str(random.random()).encode()).hexdigest()[:20]+".jpg")
        path = get_path()
        while os.path.isfile(path):
            path = get_path()

        bpy.ops.render.render()
        bpy.data.images["Render Result"].save_render(path)

        with open(path, "rb") as file:
            data = file.read()
        os.remove(path)

        self.send({"type": "render_frame", "image": data})

    def send(self, obj):
        data = zlib.compress(pickle.dumps(obj))
        len_msg = (str(len(data)) + self.padding)[:self.header].encode()

        packets = []
        while data:
            curr_len = min(len(data), self.packet_size)
            packets.append(data[:curr_len])
            data = data[curr_len:]

        self.conn.send(len_msg)
        for packet in packets:
            self.conn.send(packet)

    def recv(self):
        len_msg = b""
        while len(len_msg) < self.header:
            len_msg += self.conn.recv(self.header-len(len_msg))

        length = int(len_msg)
        data = b""
        while len(data) < length:
            curr_len = min(self.packet_size, length-len(data))
            data += self.conn.recv(curr_len)

        return pickle.loads(zlib.decompress(data))
