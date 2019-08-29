import stat
import os
import shutil
dirs = os.listdir()
dirList= []

for dir in dirs:
    if os.path.isdir(dir):
        dirList.append(int(dir))
dirList.sort()
dirList.reverse()
print(dirList)
for dir in dirList:
    shutil.move(str(dir), str(dir+50))
    #os.chmod(dir, stat.S_IRUSR | stat.S_IWGRP | stat.S_IWOTH)
