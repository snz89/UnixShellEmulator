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
python emulator.py -u myuser -c mycomputer myfilesystem.tar -l mylog.csv -s myscript.txt 
```

## Docker Usage

You can easily run the UnixShellEmulator using Docker. This allows for a consistent environment without needing to install dependencies on your local machine.

### Prerequisites

- Install Docker on your system. Follow the instructions at [Docker Installation](https://docs.docker.com/get-docker/).

### Build the Docker Image

Navigate to the project directory where your `Dockerfile` is located, and build the Docker image with the following command:

```bash
docker build -t unixshell-emulator .
```

### Run the Emulator

To run the emulator, you can mount a local directory containing your tar archive and log file. Use the following command:

```bash
docker run -it --rm -v /path/to/local/directory:/app/data unixshell-emulator /app/data/filesystem.tar -u [username] -c [computername] -l /app/data/logfile.csv -s /app/data/script.txt
```