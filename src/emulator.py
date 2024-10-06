import tarfile
import csv
import os
import datetime
import argparse


class Emulator:
    def __init__(self, username, computername, filesystem, log_file, script):
        self.current_path = "/"
        self.username = username
        self.computername = computername
        self.filesystem = tarfile.open(filesystem, "r")
        self.log_file = log_file
        self.script_file = script
        self.history = []

    def execute(self):
        if self.script_file:
            self.__run_script(self.script_file)
        while True:
            command = input(
                f'{self.username}@{self.computername}:{self.current_path} ')
            self.history.append(command)
            self.__log_command(command)
            self.__execute_command(command)

    def __execute_command(self, command):
        command_parts = command.split()
        command_name = command_parts[0]

        if command_name == "ls":
            path = command_parts[1] if len(
                command_parts) > 1 else self.current_path
            self.__ls(path)
        elif command_name == "cd":
            try:
                path = command_parts[1]
                self.__cd(path)
            except IndexError:
                print("cd: missing operand")
        elif command_name == "exit":
            self.filesystem.close()
            exit()
        elif command_name == "pwd":
            self.__pwd()
        elif command_name == "history":
            self.__history()
        else:
            print(f"{command_name}: command not found")

    def __ls(self, path):
        file_list = self.filesystem.getnames()

        if path.startswith("/"):
            full_path = path
        else:
            full_path = os.path.join(self.current_path, path).replace("\\", "/")

        if full_path == "/":
            result = []
            for item in file_list:
                if "/" not in item:
                    result.append(item)
                else:
                    parts = item.split("/")
                    if parts[0] not in result:
                        result.append(parts[0] + "/")
            for item in sorted(result):
                print(item)
        else:
            prefix = full_path[1:] + "/"
            result = []
            for item in file_list:
                if item.startswith(prefix) and item != prefix:
                    rest = item[len(prefix):]
                    if "/" not in rest:
                        result.append(rest)
                    else:
                        parts = rest.split("/")
                        if parts[0] not in result:
                            result.append(parts[0] + "/")
            for item in sorted(result):
                print(item)

    def __cd(self, path):
        file_list = self.filesystem.getnames()

        if path == "/":
            self.current_path = "/"
            return

        if path.startswith("/"):
            full_path = path
        else:
            full_path = os.path.join(self.current_path, path).replace("\\", "/")

        try:
            tarinfo = self.filesystem.getmember(full_path[1:])
            
            if tarinfo.isdir():
                self.current_path = full_path
            else:
                print(f"cd: {path}: Not a directory")
        except KeyError:
            print(f"cd: can't cd to {path}: No such file or directory")

    def __pwd(self):
        print(self.current_path)

    def __history(self):
        for i, command in enumerate(self.history):
            print(f"{i+1} {command}")

    def __log_command(self, command):
        with open(self.log_file, "a", newline="") as f:
            writer = csv.writer(f)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, self.username, command])
    
    def __run_script(self, script_file):
        try:
            with open(script_file, "r") as f:
                for line in f:
                    command = line.strip()
                    print(f'{self.username}@{self.computername}:{self.current_path} {command}')
                    self.history.append(command)
                    self.__log_command(command)
                    self.__execute_command(command)
        except FileNotFoundError:
            print(f"{script_file}: No such file or directory")
                    


def main():
    parser = argparse.ArgumentParser(description="Unix Shell Emulator")
    
    parser.add_argument("-u", "--user", default="localhost", help="Username")
    parser.add_argument("-c", "--computer", default="localhost", help="Username")
    parser.add_argument("filename", help="Path to the filesystem tar archive")
    parser.add_argument("-l", "--log", default="log.csv", help="Path to the logfile")
    parser.add_argument("-s", "--script", help="Path to the start script")
    
    args = parser.parse_args()
    
    emulator = Emulator(args.user, args.computer, args.filename, args.log, args.script)
    emulator.execute()


if __name__ == "__main__":
    main()
