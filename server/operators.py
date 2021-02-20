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

import threading
import ctypes
import bpy
from bpy.types import Operator
from bpy.props import BoolProperty, IntProperty, FloatProperty, StringProperty, EnumProperty
from .connection import Server
from .render import render

server = None
status = None
activated = None


class RENDERGROUP_SERVER_OT_Start(Operator):
    bl_label = "Start Server"
    bl_description = "Starts server and allows others to connect."
    bl_idname = "render_group_server.start"

    def execute(self, context):
        global server, status
        props = context.scene.render_group_server
        prefs = context.preferences.addons[__package__].preferences

        server = Server(prefs.server_ip, 5555)
        threading.Thread(target=server.start).start()

        status = "WAITING"
        return {"FINISHED"}


class RENDERGROUP_SERVER_OT_StartRender(Operator):
    bl_label = "Start Render"
    bl_description = "Starts rendering on all clients."
    bl_idname = "render_group_server.start_render"

    show_confirm: BoolProperty(default=True)

    def execute(self, context):
        global server, status
        props = context.scene.render_group_server
        prefs = context.preferences.addons[__package__].preferences

        if self.show_confirm:
            bpy.ops.render_group_server.start_render_confirm("INVOKE_DEFAULT")
            return {"CANCELLED"}

        if len(server.clients) == 0:
            self.report({"ERROR"}, "Please connect at least one client.")
            return {"CANCELLED"}

        threading.Thread(target=render, args=(props, server.clients)).start()

        status = "RENDERING"
        self.report({"INFO"}, "Rendering started.")
        return {"FINISHED"}


class RENDERGROUP_SERVER_OT_StartRenderConfirm(Operator):
    bl_label = "Start Render?"
    bl_description = "Do you really want to start the render?"
    bl_idname = "render_group_server.start_render_confirm"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Do you really want to start the render?")

    def execute(self, context):
        bpy.ops.render_group_server.start_render(show_confirm=False)
        return {"FINISHED"}


class RENDERGROUP_SERVER_OT_Activate(Operator):
    bl_label = "Activate Add-on"
    bl_description = "Activates the add-on.\nOnce activated, the add-on will forcefully crash\nBlender on exit."
    bl_idname = "render_group_server.activate"

    def execute(self, context):
        global activated
        activated = True
        return {"FINISHED"}


classes = (
    RENDERGROUP_SERVER_OT_Start,
    RENDERGROUP_SERVER_OT_StartRender,
    RENDERGROUP_SERVER_OT_StartRenderConfirm,
    RENDERGROUP_SERVER_OT_Activate,
)

def register():
    global server, status, activated

    for cls in classes:
        bpy.utils.register_class(cls)

    server = None
    status = "NOT_STARTED"
    activated = False

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    if activated:
        ctypes.pointer(ctypes.c_char.from_address(5))[0]
