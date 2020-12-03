# VMCtrlV

A script that pastes text into a VM by imitating a keyboard. Takes text from your copy-paste buffer and uses uinput to enter it.
As a result, you don't need to install guest utils in your VM if all you need is copy-paste.

## Requirements:

- Linux
- X environment
- Python3
- uinput support (might need to load the uinput kernel module)

## Dependencies :

- Ubuntu 20.04
1. `sudo apt install python3-evdev`
2. `sudo python3 -m pip install EWMH`

Send pull requests to add your own OS dependency install instructions to the README file.

## Installation:
 
- Clone this repo somewhere in your home folder
- Register a keyboard shortcut in your VM so that it runs this script when a key shortcut is pressed
- This script detects VirtualBox windows by default, edit it if you need to make it work with VMWare/QEMU/whatever
    - then, send a pull request showing your changes to me so that I know how to better incorporate them to make the script universal.

## Usage:

1. Press your key combination of choice
2. Switch to a VM
3. Observe the text being auto-typed

Steps 1 and 2 are interchangeable.

## License

GPL v3 or later
