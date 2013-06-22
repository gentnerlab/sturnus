#!/usr/bin/python
import os
import sys
import subprocess


# parser = OptionParser()

def main():
    if "VIRTUAL_ENV" not in os.environ:
        sys.stderr.write("$VIRTUAL_ENV not found.\n\n")
        # parser.print_usage()
        sys.exit(-1)
    file_path = os.path.dirname(__file__)
    subprocess.call(["pip", "install", "--requirement",
                     os.path.join(file_path, "requirements/apps.txt")])

if __name__ == "__main__":
    main()
    sys.exit(0)
