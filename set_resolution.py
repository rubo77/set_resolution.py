#!/usr/bin/env python3
import subprocess
import os
import sys
import time

#--- set default resolution below
resolution = "1680x1050"
#---

curr_dir = os.path.dirname(os.path.abspath(__file__))
datafile = curr_dir+"/procsdata.txt"
applist = [l.split() for l in open(datafile).read().splitlines()]
print(applist)
apps = [item[0] for item in applist]

def get(cmd):
    try:
        return subprocess.check_output(["/bin/bash", "-c", cmd]).decode("utf-8")
    except subprocess.CalledProcessError:
        pass

def get_pids():
    # returns pids of listed applications; seems ok
    runs = []
    for item in apps:
        pid = get("pgrep -f "+item)
        if pid != None:
            runs.append((item, pid.strip()))    
    return runs

def check_frontmost():
    # returns data on the frontmost window; seems ok
    frontmost = str(hex(int(get("xdotool getwindowfocus").strip())))
    frontmost = frontmost[:2]+"0"+frontmost[2:]
    try:
        wlist = get("wmctrl -lpG").splitlines()
        return [l for l in wlist if frontmost in l]
    except subprocess.CalledProcessError:
        pass

def front_pid():
    # returns the frontmost pid, seems ok
    return check_frontmost()[0].split()[2]

def matching():
    running = get_pids(); frontmost = check_frontmost()
    if all([frontmost != None, len(running) != 0]):
        matches = [item[0] for item in running if item[1] == frontmost[0].split()[2]]
    if len(matches) != 0:
        return matches[0]
    else:
        pass

trigger1 = matching()
    
while True:
    time.sleep(1)
    trigger2 = matching()
    if trigger2 != trigger1:
        if trigger2 == None:
            command = "xrandr -s "+resolution
        else:
            command = "xrandr -s "+[it[1] for it in applist if it[0] == trigger2][0]
        subprocess.Popen(["/bin/bash", "-c", command])
        print(command)
    trigger1 = trigger2
