# USBLanturn

USBLanturn implements usb support to the Lanturn seed checking bot I created a while back. This version of Lanturn relies on USB-botbase, which can be downloaded [here](https://github.com/fishguy6564/USB-Botbase).

## Requirements
- A hacked Switch with Atmosphere CFW installed.
- Python3 must be installed in order to use Lanturn.
- The latest discord.py API must be installed. You can install this by using the following pip command.
```bash
python -m pip install -U discord.py
```
- z3-solver must be installed as well. You can install z3-solver using the following pip command.
```bash
pip install z3-solver
```
- A usb-c to usb-a cable is required to connect your PC to your Nintendo Switch.
- Pyusb is necessary in order to communicate to the Nintendo Switch. You can install Pyusb by using the following pip command.
```bash
pip install pyusb
```
- A usb backend is necessary. Please use [Zadig](http://www.unitrunker.com/zadig.html) and install the libusbk driver to your Nintendo Switch by plugging it in while running the sys-module.
- Install libusb with [this](http://www.mediafire.com/file/wdx5lu4c37sm1cv/libusb-win32-devel-filter-1.2.6.0.exe/file).

## Installation
Once you have installed all the requirements listed above, click "Clone or download" and then click "Download ZIP". 
- Extract the contents in the ZIP to a folder.
- Edit the information in bot.py, RaidCommands.py, and DuduClient.py. I have left comments for the end user so they know what to edit.
- Save all edits and run run.bat

## Commands
- $GetSeed - Gets a user's seed and next square/star shiny frame
by a user passing their encryption constant, pid, and IVs as arguments.
- $GetFrameData - Gets a user's next square/star shiny frame by a
user passing their already generated seed as an argument.
- $CheckMySeed - Queues up the invoker and initiates the Dudu Clone modules.
It communicates to the DuduClient script via the communicate.bin file. Please
do not trash any files when downloading them.
- $greet - Sends a cute message depending on what the developer sets it to.
- $CheckQueueSize - Reports the amount of people currently in the queue
- $logout - For the admin only. Will turn off the bot for testing.
