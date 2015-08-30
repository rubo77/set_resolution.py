#!/usr/bin/env python3
import subprocess
import os
import sys
import time

#--- set default settings below
defaultResolution = "3200x1800"
defaultScalingFactor = 2
#---

curr_dir = os.path.dirname(os.path.abspath(__file__))
datafile = curr_dir+"/procsdata.txt"
applist = [l.split() for l in open(datafile).read().splitlines()]
apps = [item[0] for item in applist]

def execute(cmd):
    try:
        return subprocess.check_output(["/bin/bash", "-c", cmd], stderr=subprocess.STDOUT).strip()
    except subprocess.CalledProcessError:
        pass

def get_pids():  # returns pids of listed applications; seems ok
    runs = []
    for item in apps:
        pid = execute("pgrep -f "+item)
        if pid != None:
            runs.append(pid.strip().splitlines())
    return runs  # list of lists of pids for each app

def check_frontmost():
    frontmost = execute("xdotool getactivewindow getwindowpid")
    if frontmost != None:
        return(frontmost.strip())
        
    # if getwindowpid fails, try getting window name and pass to ps
    windowName = execute("xdotool getactivewindow getwindowname").lower()
    frontmost = execute("ps ax | pgrep " + windowName)
    if frontmost != None:
        return(frontmost)
    
    # if all else fails, try wmctrl
    frontmost = str(hex(int(execute("xdotool getwindowfocus"))))
    frontmost = frontmost[:2]+"0"+frontmost[2:]
    try:
        wlist = execute("wmctrl -lpG").splitlines()
        return [l for l in wlist if frontmost in l][0].split()[2]
    except subprocess.CalledProcessError:
        pass

def matching():  # nakijken
    running = get_pids()
    frontmost = check_frontmost()
    if all([len(frontmost) != 0, len(running) != 0]):      
        for index, elem in enumerate(running):
            if frontmost in elem:
                return(index)
        return(None)
    else:
        pass


def set_resolution(res):
    command = "xrandr -s " + res
    subprocess.Popen(["/bin/bash", "-c", command])
    print(command)


def set_scaling_factor(n):
    execute("gsettings set org.gnome.desktop.interface scaling-factor "+str(n))
    return None
    
# TODO: test using user downloaded fonts on Gnome 3 
# TODO: test on Unity
def set_mouse_size(n):
    execute("gsettings set org.gnome.desktop.interface cursor-size "+str(48/int(n)))
    return None

while True:
    currentWindow = check_frontmost()  # get front window
    time.sleep(0.5)
    if currentWindow != check_frontmost():  # test for change
        idx = matching()  # find matching pids
        if idx != None:  # if in applist, set to desired resolution
            set_resolution(applist[idx][1])
            set_scaling_factor(applist[idx][2])
            set_mouse_size(applist[idx][2])
        else:  # if not in app list, reset to default
            set_resolution(defaultResolution)
            set_scaling_factor(defaultScalingFactor)
            set_mouse_size(defaultScalingFactor)

