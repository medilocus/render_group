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

import bpy
from bpy.types import Panel


class RENDERGROUP_SERVER_PT_Main(Panel):
    bl_label = "Render Group - Server"
    bl_idname = "RENDERGROUP_SERVER_PT_Main"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        from .operators import server, status
        props = context.scene.render_group_server
        prefs = context.preferences.addons[__package__].preferences
        layout = self.layout

        if status == "NOT_STARTED":
            layout.prop(prefs, "server_ip")
            layout.operator("render_group_server.start")

        elif status == "WAITING":
            layout.label(text="Click \"Start\" when ready.")
            if props.show_clients:
                col = layout.column(align=True)
                col.prop(props, "show_clients", text="Hide Clients", toggle=True, icon="TRIA_DOWN")
                box = col.box()
                for c in server.clients:
                    box.label(text=f"{c.name}, {c.addr[0]}")
            else:
                layout.prop(props, "show_clients", text="Show Clients", toggle=True, icon="TRIA_RIGHT")


classes = (
    RENDERGROUP_SERVER_PT_Main,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
