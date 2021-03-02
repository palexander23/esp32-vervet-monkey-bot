# ESP32 Robot Software

## Software Requirements
* make
* python3.x
* ampy
* PuTTY

### Make
Used in the build system.
Install make for Windows from the link below:

http://gnuwin32.sourceforge.net/packages/make.htm

### python3.x
Used to install/run ampy.
Installed from the link below:

python.org

### Ampy
Used to communicate and upload files to the ESP32
Installed with the following command:
```bash
python -m pip install adafruit-ampy
```

### PuTTY
Used to link to the MicroPython REPL on the board.
Install from the following link:

https://www.putty.org/


## PATH Setup

You may need to add the Python/Script directory and the make/bin directory to your PATH variable.
The locations of these directories will be specific to your installation.

## Setting Up the ESP32
Before uploading code to the ESP32, the proprietary micropython environment built for this project must be uploaded.
See the `README.md` in the micropython_port directory.

## Building the software
Running the following command should upload the python code and open a PuTTY prompt.
You have to reset the board after the upload is complete.