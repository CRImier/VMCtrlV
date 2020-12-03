#!/usr/bin/env python3
"""
    Copyright Arsenijs Picugins, 2020

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import sys
import string
import atexit
import subprocess
from time import sleep

from ewmh import EWMH
from evdev import ecodes, UInput

enter_with_shift = True

################################################################
# Flag to avoid running more than one copy of the script at once
################################################################

def create_flag():
    with open("/tmp/vmctrlv.flag", "w") as f:
        f.write(" ")

def remove_flag():
    os.remove("/tmp/vmctrlv.flag")

def flag_exists():
    os.path.exists("/tmp/vmctrlv.flag")

######################
# Character input code
######################

# currently only supports ASCII, sorry.
# also in part because uinput can't really emulate keyboard layouts.
# As a sidenote, this will break with en_GB keyboard layout...
# ...why would you use that one, anyway.

chars_need_shift = {"~":"GRAVE", "!":"1", "@":"2", "#":"3", "$":"4", "%":"5", "^":"6", "&":"7", \
                    "*":"8", "(":"9", ")":"0", "_":"MINUS", "+":"EQUAL", "\"":"APOSTROPHE", \
                    "|":"BACKSLASH", ":":"SEMICOLON", "?":"SLASH", ">":"DOT", "<":"COMMA"}

special_char_keys = {" ":"SPACE", "`":"GRAVE", "-":"MINUS", "=":"EQUAL","'":"APOSTROPHE", \
                     "\\":"BACKSLASH", ";":"SEMICOLON", "/":"SLASH", ".":"DOT", ",":"COMMA"}

if enter_with_shift:
    chars_need_shift["\n"] = "ENTER"
else:
    special_char_keys["\n"] = "ENTER"


def write_text(text, uinput):
    shift_pressed = False
    for char in text:
        # checking if pressing shift is necessary
        # this script holds the shift until it's no longer necessary
        # just like a human would
        if (char in string.ascii_uppercase or char in chars_need_shift):
            if not shift_pressed:
                uinput.write(ecodes.EV_KEY, ecodes.ecodes['KEY_LEFTSHIFT'], 1)
                shift_pressed = True
        elif shift_pressed:
            uinput.write(ecodes.EV_KEY, ecodes.ecodes['KEY_LEFTSHIFT'], 0)
            shift_pressed = False
        if char in string.ascii_letters or char in string.digits:
            key = "KEY_{}".format(char.upper())
        elif char in chars_need_shift:
            key = "KEY_{}".format(chars_need_shift[char])
        elif char in special_char_keys:
            key = "KEY_{}".format(special_char_keys[char])
        else:
            print("Unrecognized character: {} ({})!".format(char, hex(char)))
            continue
        uinput.write(ecodes.EV_KEY, ecodes.ecodes[key], 1)
        sleep(0.001)
        uinput.write(ecodes.EV_KEY, ecodes.ecodes[key], 0)
        uinput.syn()
        sleep(0.01)
    if shift_pressed:
        uinput.write(ecodes.EV_KEY, ecodes.ecodes['KEY_LEFTSHIFT'], 0)
        shift_pressed = False
        uinput.syn()

###################
# VM detection code
###################

def is_vm(window_name):
    return window_name.endswith("Oracle VM VirtualBox")

################################
# Copy-paste buffer parsing code
################################

default_type = "STRING"

def get_available_buffer_types():
    try:
        output = subprocess.check_output(["xclip", "-o", "-t", "TARGETS"])
    except CalledProcessError as e:
        return []
    else:
        output = output.decode('utf-8')
        return [line.strip() for line in output.split("\n") if line.strip()]

def get_buffer_contents(buffer_type):
    try:
        output = subprocess.check_output(["xclip", "-o", "-t", buffer_type])
    except CalledProcessError as e:
        print("Error calling xclip! {} {}".format(repr(e.output), e.return_code))
        return ""
    else:
        return output.decode('utf-8')

################
# Main functions
################

if flag_exists():
    print("Flag file exists!")
    sys.exit(1)

create_flag()

wmm = EWMH()
uinput = UInput(name="VMCtrlV")

def cleanup():
    remove_flag()
    uinput.close()

atexit.register(cleanup)

def main():
    # wait until the VM window is the active window
    switched_to_vm = False
    while not switched_to_vm:
        name = wmm.getWmName(wmm.getActiveWindow())
        name = name.decode('utf-8')
        if is_vm(name):
            switched_to_vm = True
        else:
            sleep(1)
    # we have switched to the VM!
    # let's get the latest copy-paste buffer first
    types = get_available_buffer_types()
    if default_type not in types:
        # unsupported copy-paste buffer format
        print("Copy-paste format unsupported - {}".format(",".join(types)))
        return
    buffer_contents = get_buffer_contents(default_type)
    if not buffer_contents:
        print("Buffer contents empty or error has occured")
        return
    # now let's type the buffer using the fake keyboard we made
    write_text(buffer_contents, uinput)

main()

