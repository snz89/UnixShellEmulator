import tarfile
import csv
import os
import datetime
import sys


class Emulator:
    def __init__(self, username, computername, filesystem, log_file, script):
        self.current_path = "/"
        self.username = username
        self.computername = computername
        try:
            self.filesystem = tarfile.open(filesystem, "r")
        except FileNotFoundError:
            print(f"Error: Filesystem file '{filesystem}' not found. Exiting.")
            sys.exit(1)
        self.log_file = log_file
        self.script_file = script
        self.history = []

    def execute(self):
        if self.script_file:
            self.run_script(self.script_file)
        while True:
            command = input(
                f'{self.username}@{self.computername}:{self.current_path} ')
            self.history.append(command)
            self.log_command(command)
            self.execute_command(command)

    def execute_command(self, command):
        """Parses and executes the given shell command."""
        command_parts = command.strip().split()

        if not command_parts:
            print("No command entered. Please try again.")
            return

        command_name = command_parts[0]

        if command_name == "ls":
            path = command_parts[1] if len(
                command_parts) > 1 else self.current_path
            self.ls(path)
        elif command_name == "cd":
            try:
                path = command_parts[1]
                self.cd(path)
            except IndexError:
                print("cd: missing operand")
        elif command_name == "exit":
            self.filesystem.close()
            sys.exit()
        elif command_name == "pwd":
            self.pwd()
        elif command_name == "history":
            self.print_history()
        else:
            print(f"{command_name}: command not found")

    def ls(self, path):
        """Lists the contents of the specified directory within the virtual filesystem."""
        file_list = self.filesystem.getnames()

        if path.startswith("/"):
            full_path = path
        else:
            full_path = os.path.join(
                self.current_path, path).replace("\\", "/")

        if full_path == "/":
            result = set()
            for item in file_list:
                tarinfo = self.filesystem.getmember(item)
                if "/" not in item:
                    result.add(item + ("/" if tarinfo.isdir() else ""))
                else:
                    parts = item.split("/")
                    result.add(
                        parts[0] + ("/" if self.filesystem.getmember(parts[0]).isdir() else ""))
            for item in sorted(list(result)):
                print(item)
        else:
            try:
                tarinfo = self.filesystem.getmember(full_path[1:])
                prefix = full_path[1:] + "/"
                result = set()
                for item in file_list:
                    if item.startswith(prefix) and item != prefix:
                        rest = item[len(prefix):]
                        tarinfo = self.filesystem.getmember(item)
                        if "/" not in rest:
                            result.add(rest + ("/" if tarinfo.isdir() else ""))
                        else:
                            parts = rest.split("/")
                            result.add(
                                parts[0] + ("/" if self.filesystem.getmember(prefix + parts[0]).isdir() else ""))
                for item in sorted(list(result)):
                    print(item)
            except KeyError:
                print(f"ls: {path}: No such file or directory")

    def cd(self, path):
        """Changes the current directory within the virtual filesystem."""
        if path == "/":
            self.current_path = "/"
            return

        if path.startswith("/"):
            full_path = path
        else:
            full_path = os.path.join(
                self.current_path, path).replace("\\", "/")

        try:
            tarinfo = self.filesystem.getmember(full_path[1:])

            if tarinfo.isdir():
                self.current_path = full_path
            else:
                print(f"cd: {path}: Not a directory")
        except KeyError:
            print(f"cd: can't cd to {path}: No such file or directory")

    def pwd(self):
        """Prints the current working directory within the virtual filesystem."""
        print(self.current_path)

    def print_history(self):
        """Prints the command history with line numbers."""
        for i, command in enumerate(self.history):
            print(f"{i+1} {command}")

    def log_command(self, command):
        """Logs the executed command with timestamp and username to a CSV file."""
        with open(self.log_file, "a", newline="") as f:
            writer = csv.writer(f)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, self.username, command])

    def run_script(self, script_file):
        """Executes commands from a script file."""
        try:
            with open(script_file, "r") as f:
                for line in f:
                    command = line.strip()
                    print(
                        f'{self.username}@{self.computername}:{self.current_path} {command}')
                    self.history.append(command)
                    self.log_command(command)
                    self.execute_command(command)
        except FileNotFoundError:
            print(f"{script_file}: No such file or directory")
