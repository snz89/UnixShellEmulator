import tarfile
import csv
import os
import datetime

class Emulator:
    def __init__(self, username, computername, filesystem, log_file):
        self.current_path = "/"
        self.username = username
        self.computername = computername
        self.filesystem = tarfile.open(filesystem, "r")
        self.log_file = log_file
        self.history = []
    
    def execute(self):
        while True:
            command = input()
            self.history.append(command)
            self.__log_command(command)
            self.__execute_command(command)
    
    def __execute_command(self, command):
        if command == "ls":
            self.__ls()
        elif command == "cd":
            self.__cd()
        elif command == "exit":
            self.__exit()
        elif command == "pwd":
            self.__pwd()
        elif command == "history":
            self.__history()
        else:
            print(f"{command}: command not found")

    def __ls(self):
        pass
    
    def __cd(self, path):
        if path == "/":
            self.current_path = "/"
            return
        
        if path.startswith("/"):
            full_path = path
        else:
            full_path = os.path.join(self.current_path, path)
    
    def __exit(self):
        pass
    
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

def main():
    pass

if __name__ == "__main__":
    main()