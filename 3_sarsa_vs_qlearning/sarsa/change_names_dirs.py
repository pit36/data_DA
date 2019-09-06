import os
import argparse
parser = argparse.ArgumentParser(description='Changing Folders title')
parser.add_argument('--number', default= 50, type=int, help='How many should be incremented')
args = parser.parse_args()
dirs = os.listdir()
dirList= []

for dir in dirs:
    if os.path.isdir(dir):
        dirList.append(dir)

for dir in dirList:
    os.rename(dir, str(int(dir)+args.number))
