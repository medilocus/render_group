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
from bpy.types import PropertyGroup
from bpy.props import BoolProperty, IntProperty, FloatProperty, StringProperty, EnumProperty, PointerProperty


class RENDERGROUP_SERVER_Props(PropertyGroup):
    show_clients: BoolProperty(
        name="Connected Clients",
        description="Whether to show connected clients.",
        default=True
    )

    frame_start: IntProperty(
        name="Frame Start",
        description="Starting frame of render.",
        default=0, soft_min=0, soft_max=100000
    )

    frame_end: IntProperty(
        name="Frame End",
        description="Ending frame of render.",
        default=1000, soft_min=0, soft_max=100000
    )

    frame_step: IntProperty(
        name="Frame Step",
        description="Step of frames in render.",
        default=1, min=1, soft_max=10
    )

    out_path: StringProperty(
        name="Output Path",
        description="Output directory of all images rendered.",
        subtype="DIR_PATH"
    )


classes = (
    RENDERGROUP_SERVER_Props,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.render_group_server = PointerProperty(type=RENDERGROUP_SERVER_Props)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.render_group_server
