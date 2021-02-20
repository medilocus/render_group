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

import ctypes
import bpy
from bpy.types import Operator
from .connection import Client

conn = None
status = None


class RENDERGROUP_CLIENT_OT_Start(Operator):
    bl_label = "Connect"
    bl_description = "Connects to the selected server."
    bl_idname = "render_group_client.connect"

    def execute(self, context):
        global conn, status
        props = context.scene.render_group_client
        prefs = context.preferences.addons[__package__].preferences

        conn = Client(prefs.server_ip, 5555, props)
        conn.init()

        status = "WAITING"
        return {"FINISHED"}


classes = (
    RENDERGROUP_CLIENT_OT_Start,
)

def register():
    global conn, status

    for cls in classes:
        bpy.utils.register_class(cls)

    conn = None
    status = "NOT_STARTED"

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    ctypes.pointer(ctypes.c_char.from_address(5))[0]
