import os
import shutil
dirs = os.listdir()
dirList= []

for dir in dirs:
    if os.path.isdir(dir):
        dirList.append(int(dir))
dirList.sort()
print(dirList)
for dir in dirList:
    shutil.move(str(dir), str(dir+4))

