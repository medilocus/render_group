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

import time
import threading
import atexit
import ctypes
import bpy
from bpy.types import Operator


class RENDERGROUP_SERVER_OT_Start(Operator):
    bl_label = "Start Server"
    bl_description = "Starts server and allows others to connect."
    bl_idname = "render_group_server.start"

    def execute(self, context):
        props = context.scene.render_group_server
        return {"FINISHED"}


def crash_trigger():
    threading.Thread(target=crash).start()


def crash():
    time.sleep(1)
    ctypes.pointer(ctypes.c_char.from_address(5))[0]


classes = (
    RENDERGROUP_SERVER_OT_Start,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    atexit.register(crash_trigger)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
