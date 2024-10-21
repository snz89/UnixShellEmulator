import argparse

from emulator import Emulator

def main():
    parser = argparse.ArgumentParser(description="Unix Shell Emulator")

    parser.add_argument("-u", "--user", default="localhost", help="Username")
    parser.add_argument("-c", "--computer",
                        default="localhost", help="Username")
    parser.add_argument("filename", help="Path to the filesystem tar archive")
    parser.add_argument("-l", "--log", default="log.csv",
                        help="Path to the logfile")
    parser.add_argument("-s", "--script", help="Path to the start script")

    args = parser.parse_args()

    emulator = Emulator(args.user, args.computer,
                        args.filename, args.log, args.script)
    emulator.execute()


if __name__ == "__main__":
    main()
