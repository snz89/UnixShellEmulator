# UnixShellEmulator
 
This project provides a basic Unix shell emulator that operates on a tar archive as a virtual filesystem.

## Features

* Emulates basic Unix commands: `ls`, `cd`, `pwd`, `exit`, `history`.
* Operates on a tar archive without unpacking.
* Customizable username and computer name in the prompt.
* Logging of commands with timestamps and username.
* Support for executing a startup script.

## Usage

To run the emulator, use the following command:

```bash
python emulator.py -u [username] -c [computername] [filesystem.tar] -l [logfile.csv] -s [script.txt]
```

*  `-u, --user`:  Username (default: user)
*  `-c, --computer`: Computer name (default: localhost)
*  `<filesystem.tar>`: **Required**. Path to the tar archive containing the virtual filesystem.
*  `-l, --log`: Path to the log file (default: log.csv).
*  `-s, --script`: Path to a script file to execute on startup.

**Example:**

```bash
python emulator.py -u myuser -c mycomputer myfilesystem.tar -l mylog.csv -s myscript.sh 
```
