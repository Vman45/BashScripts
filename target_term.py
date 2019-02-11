#!/usr/bin/env python3

import subprocess
import os
import sys
import time
import getpass
#--- set your terminal below
application = "gnome-terminal"
#---

option = sys.argv[1]
data = os.environ["HOME"]+"/.term_list"

def current_windows():
    w_list = subprocess.check_output(["wmctrl", "-lp"]).decode("utf-8")
    w_lines = [l for l in w_list.splitlines()]
    try:
        pid = subprocess.check_output(["pgrep", application]).decode("utf-8").strip()
        return [l for l in w_lines if str(pid) in l]
    except subprocess.CalledProcessError:
        return []

def arr_windows(n):
    w_count1 = current_windows()
    for requested in range(n):
        subprocess.Popen([application])
    called = []
    while len(called) < n:
        time.sleep(1)
        w_count2 = current_windows()
        add = [w for w in w_count2 if not w in w_count1]
        [called.append(w.split()[0]) for w in add if not w in called]
        w_count1 = w_count2

    return called

def run_intterm(w, command):
    subprocess.call(["xdotool", "windowfocus", "--sync", w])
    subprocess.call(["xdotool", "type", command+"\n"])

def addWindows():
    n = int(sys.argv[2])
    new = arr_windows(n)
    for w in new:
        open(data, "a").write(w+"\n")

# ----------------------------- Command functions ------------------------------
def add():
    addWindows()

def set():
    open(data, "w").write("")
    addWindows()

def run():
    t_term = open(data).read().splitlines()[int(sys.argv[2])-1]
    command = (" ").join(sys.argv[3:])
    run_intterm(t_term, command)

def install():
    password = getpass.getpass("Admin Password: ");
    w_count2 = arr_windows(1)
    t_term = w_count2[0]
    run_intterm(t_term, "sudo apt-get install wmctrl xdotool")
    run_intterm(t_term, password)
    run_intterm(t_term, "sudo cp ./target_term.py /bin/target_term")
    run_intterm(t_term, "sudo chmod +x /bin/target_term")
    time.sleep(10)
    run_intterm(t_term, "exit")

def count():
    print(len(open(data).read().splitlines()))

eval(option + "()")