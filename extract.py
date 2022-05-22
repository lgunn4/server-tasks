import shutil
import os
import argparse
import sys

# Define arguments for source and destination
parser = argparse.ArgumentParser(prog=sys.argv[0], usage='%(prog)s [options]')
parser.add_argument("-s","--source",action='append',help="File source directory",required=True)
parser.add_argument("-d","--destination",action='append',help="File destination directory",required=True)

args = parser.parse_args()

# Define the source and destination path
source = args.source[0]
destination = args.destination[0]
CWD = os.getcwd()

# code to move the files from sub-folder to main folder.
folders = os.listdir(source)

for folder in folders:
    if os.path.isdir(folder):

        files = os.listdir(folder)
        for file in files:
            os.rename(os.path.join(CWD, folder, file), os.path.join(CWD, destination, file))
        os.rmdir(folder)
print("Files Moved")