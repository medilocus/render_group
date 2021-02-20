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


def render(props, clients):
    frame_start = props.frame_start
    frame_end = props.frame_end
    frame_step = props.frame_step
    out_path = props.out_path
    frames = list(range(frame_start, frame_end+1, frame_step))

    for c in clients:
        c.send({"type": "render_starting"})

    while len(frames) > 0:
        time.sleep(0.1)
        for c in clients:
            if not c.busy:
                c.render_frame(frames.pop(0), out_path)
