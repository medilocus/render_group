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

import sys
import os
import time
import threading
from datetime import datetime

done = None
curr_frame = None


def render(props, clients):
    global done, curr_frame

    frame_start = props.frame_start
    frame_end = props.frame_end
    frame_step = props.frame_step
    out_path = props.out_path
    frames = list(range(frame_start, frame_end+1, frame_step))
    num_total = len(frames)

    done = False
    curr_frame = frame_start
    total_rendered = 0

    for c in clients:
        c.send({"type": "render_starting"})

    while len(frames) > 0:
        update_status(clients, total_rendered+1, num_total)
        time.sleep(0.5)

        for c in clients:
            if not c.busy:
                threading.Thread(target=c.render_frame, args=(frames.pop(0), out_path)).start()
                total_rendered += 1
                if len(frames) > 0:
                    curr_frame = frames[0]
                time.sleep(0.01)

    done = True


def update_status(clients, frames_rendered, num_to_render):
    date = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    if sys.platform == "linux" or sys.platform == "darwin":
        clear = lambda: os.system("clear")
    elif sys.platform == "windows":
        clear = lambda: os.system("cls")
    else:
        clear = lambda: print("\n"*15)

    clear()
    sys.stdout.write(f"Render Group - Status update at {date}\n")
    sys.stdout.write(f"- {frames_rendered} of {num_to_render} frames rendered ({int(frames_rendered/num_to_render*1000)/10})%\n")
    sys.stdout.write(f"- {len(clients)} clients connected.\n")
    for c in clients:
        if c.busy:
            status = f"Rendering frame {c.frame}"
        else:
            status = "Idle"
        sys.stdout.write(f"    - {c.name}: {status}\n")

    sys.stdout.flush()
