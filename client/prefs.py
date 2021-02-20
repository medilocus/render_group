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
from bpy.types import AddonPreferences
from bpy.props import BoolProperty, IntProperty, FloatProperty, StringProperty, EnumProperty, PointerProperty


class RENDERGROUP_CLIENT_Prefs(AddonPreferences):
    bl_idname = __package__

    server_ip: StringProperty(
        name="Server IP",
        description="IP address to connect to.",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "server_ip")


classes = (
    RENDERGROUP_CLIENT_Prefs,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
