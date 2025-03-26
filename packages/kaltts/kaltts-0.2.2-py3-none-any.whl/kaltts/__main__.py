import sys
from . import synthesize

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '-v' or sys.argv[1] == '--version':
            print("kaltts version 0.2.1")
        else:
            print("Unknown command")
    else:
        print("Usage: kaltts -v")

if __name__ == "__main__":
    main()
