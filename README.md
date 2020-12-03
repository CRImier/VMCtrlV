# VMCtrlV

A script that pastes text into a VM by imitating a keyboard. Takes text from your copy-paste buffer and uses uinput to enter it.

## Reasons:

- You don't need to install guest utils in your VM if all you need is copy-paste.
- You don't leak all the host OS clipboard contents to the VM
  - VirtualBox auto-syncs host OS clipboard contents to the VM OS, even when the VM isn't active. As a result, software running in the VM can snoop on the host OS clipboard contents, which is a security flaw.

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
- Register a keyboard shortcut in your WM (window manager) so that it runs this script when a key shortcut is pressed
- This script detects VirtualBox windows by default, edit it if you need to make it work with VMWare/QEMU/whatever
    - then, send a pull request showing your changes to me so that I know how to better incorporate them to make the script universal.

## Usage:

1. Press your key combination of choice
2. Switch to a VM
3. Observe the text being auto-typed

Steps 1 and 2 are interchangeable.

Also, if you're already in the VM while pressing the key combination, release all shortcut combination keys quickly
to avoid cursed stuff from happening.

## License

GPL v3 or later
