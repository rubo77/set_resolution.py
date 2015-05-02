#!/usr/bin/env python3
import subprocess
import os
import time

#--set the default resolution below (mind the quotes)
default = "3200x1800"
#---

# read the datafile
curr_dir = os.path.dirname(os.path.abspath(__file__))
datafile = curr_dir+"/set_resolution.conf"
procs_data = [l.split() for l in open(datafile).read().splitlines() if not l == "\n"]
procs = [pdata[0] for pdata in procs_data]

def get(command):
    return subprocess.check_output(["/bin/bash", "-c", command]).decode("utf-8")

def check_active():
    matches = []
    for p in procs:
        try:
            matches.append([p, get("pgrep -f "+p).strip()])
        except subprocess.CalledProcessError:
            pass
    return matches

def get_res():
    xr = get("xrandr").split()
    pos = xr.index("current")
    return ("x").join([xr[pos+1], xr[pos+3].replace(",", "")])

def get_frontmost():
    try:
        fm = str(hex(int(get("xdotool getwindowfocus"))))
        return fm[:2]+"0"+fm[2:]
    except subprocess.CalledProcessError:
        pass

def get_pidlist():
    return [l.split()[:3] for l in get("wmctrl -lp").splitlines()]

frontmost1 = get_frontmost()
while True:
    time.sleep(2)
    frontmost2 = get_frontmost()
    if all([frontmost2 != frontmost1, frontmost2 != None]):
        pids = get_pidlist(); relevant = check_active()
        frontmost_pid = [w[2] for w in pids if w[0] == frontmost2]
        time.sleep(0.1)
        frontmost_pid = frontmost_pid[0]
        match = [m[0] for m in relevant if m[1] == frontmost_pid]
        try:
            req = [d[1] for d in procs_data if d[0] == match[0]][0]
        except IndexError:
            req = default
        current = get_res()
        if current != req:
            subprocess.call(["xrandr", "-s", req])
    frontmost1 = frontmost2
