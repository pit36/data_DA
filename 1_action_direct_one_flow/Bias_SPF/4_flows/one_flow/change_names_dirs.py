import os

dirs = os.listdir()
dirList= []

for dir in dirs:
    if os.path.isdir(dir):
        dirList.append(dir)

for dir in dirList:
    os.rename(dir, str(int(dir)+50))
