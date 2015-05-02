# set_resolution.py

A background script to automatically set the resolution *per application*, while you can set different resolutions for different (multiple) applications at once.

It can handle different applications with a different (required) resolution, running at the same time. The background script will keep track of what is the front most application, and will set the resolution accordingly. It also works fine with <kbd>Alt</kbd>+<kbd>Tab</kbd>.

Note that this behaviour might be annoying if you switch a lot between the desktop and listed applications; the frequent resolution switch might be too much.

An example of a *default* resolution of `3200x1800`:

![enter image description here][1]

Running `gedit`, automatically changing to `640x480`:

![enter image description here][2]

Running `gnome-terminal`, automatically changing to `1280x1024`:

![enter image description here][3]

When the application is closed, the resolution is automatically set back to `3200x1800`

###Install

    sudo apt-get install wmctrl xdotool

###How to use
1. Copy the script below into an empty file, save it as `set_resolution.py`
2. In the head of the script, set your default resolution, in the line:

        #--- set the default resolution below
        default = "3200x1800"
        #---

3. In *the very same directory* (folder), create a textfile, *exactly* named: `set_resolution.conf`. In this textfile, set the desired application or process, followed by a space, followed by the desired resolution. One application or script per line, looking like:

 ![enter image description here][4]
4. Run the script by the command:

        python3 ./set_resolution.py

###Note
The script use `pgrep -f <process>`, which catches all matches, including scripts. The possible downside is that it can cause name clashes when opening a file with the same name as the process.

If you run into issues like that, change:

    matches.append([p, subprocess.check_output(["pgrep", "-f", p]).decode("utf-8")])

into:

    matches.append([p, subprocess.check_output(["pgrep", p]).decode("utf-8")])

###Explanation
When the script starts, it reads the file in which you defined your applications and their corresponding desired screen resolutions.

It then keeps an eye on the running processes (running `pgrep -f <process>` for each of the applications) and sets the resolution if the application starts up.

When `pgrep -f <process>` does not produce output for any of the listed applications, it sets the resolution to "default".


###Notes
- Although I have it running for several hours without an error now, please test it thoroughly. If an error might occur, please leave a comment here: http://askubuntu.com/a/615754/34298
- The script -as it is- works on a single monitor setup.


  [1]: http://i.stack.imgur.com/sFVis.png
  [2]: http://i.stack.imgur.com/WKCCH.png
  [3]: http://i.stack.imgur.com/eM6Wh.png
  [4]: http://i.stack.imgur.com/ppvfe.png
