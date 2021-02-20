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

bl_info = {
    "name": "Render Group - Client",
    "description": "Client of Render Group",
    "author": "Medilocus",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Scene > Render Group - Client",
    "warning": "",
    "doc_url": "https://github.com/medilocus/render_group",
    "bug_url": "https://github.com/medilocus/render_group/issues",
    "category": "Render"
}

from . import prefs
from . import props
from . import operators
from . import ui

def register():
    prefs.register()
    props.register()
    operators.register()
    ui.register()

def unregister():
    prefs.unregister()
    props.unregister()
    operators.unregister()
    ui.unregister()
