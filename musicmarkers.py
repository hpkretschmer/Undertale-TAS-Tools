# Usage: musicmarkers.py <input file> <output file> <starting frame>
# Press space to start recording markers. 
# Press any key except space while recording to add a marker at the current frame.
# Press space again to stop recording markers and exit.

# Markers are saved as a forward slash in the input file. You can change this below.
# Use https://www.cl.cam.ac.uk/~mgk25/ucs/keysymdef.h as reference for keycodes.
MARKER_KEYCODE = "2f" # Forward slash

# Adjust the movie framerate and recording input delay if needed.
FRAMERATE = 30.0 # Frames per second
INPUT_DELAY = 0.1 # Seconds

import sys
import os
from pynput import keyboard
import time

if len(sys.argv) != 4 or sys.argv[1] in ["-h", "--help"]:
    print("Usage: musicmarkers.py <input file> <output file> <starting frame>")
    exit()

if not os.path.isfile(sys.argv[1]):
    print(f"Input file '{sys.argv[1]}' does not exist")
    exit()

recording = False
markers = []
starttime = float("nan")

def on_press(key):
    global recording, markers, starttime
    if recording:
        if key == keyboard.Key.space:
            return False
        markers.append(time.time() - starttime)
        print(f"Marker added at {markers[-1]} seconds")
    else:
        if key == keyboard.Key.space:
            starttime = time.time()
            recording = True
            print("Recording started")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

print("Recording stopped")
# print(f"Markers: {markers}")
if len(markers) == 0:
    print("No markers recorded, exiting")
    exit()
# check if markers are sorted
assert(all(mi <= mj for mi, mj in zip(markers, markers[1:])))

inputs = open(sys.argv[1]).read().splitlines()
outputfile = open(sys.argv[2], "w")

for line in inputs[:int(sys.argv[3])]:
    outputfile.write(line + "\n")

crttime = INPUT_DELAY
markeridx = 0

for i, line in enumerate(inputs[int(sys.argv[3]):]):
    # if this frame has a different framerate than the movie framerate
    if (tpos := line.find("T")) != -1:
        # parse the framerate of this frame and add the correct amount of time
        cpos = line.find(":", tpos)
        assert(cpos != -1)
        # print(line, tpos)
        # print(f"Frame time: {line[cpos+1:-1]} / {line[tpos+1:cpos]}")
        crttime += float(line[cpos+1:-1]) / float(line[tpos+1:cpos])
    else:
        crttime += 1.0 / FRAMERATE
    # if we have a marker for this frame
    if markeridx < len(markers) and  crttime >= markers[markeridx]:
        # parse the keyboard section of this frame and add the marker
        ppos = line.find("|", 1)
        assert(ppos != -1)
        if ppos == 2:
            line = line[:ppos] + MARKER_KEYCODE + line[ppos:]
        else:
            line = line[:ppos] + ":" + MARKER_KEYCODE + line[ppos:]
        markeridx += 1
        print(f"Marker added to frame {i+int(sys.argv[3])}: {line}")
    outputfile.write(line + "\n")

if markeridx < len(markers):
    print(f"Warning: {len(markers) - markeridx} markers were not added to the output file")

outputfile.close()
