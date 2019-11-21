import stat
import os

dirs = os.listdir()
dirList= []
allState = stat.S_IRUSR | stat.S_IXUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_IWOTH | \
           stat.S_IXOTH | stat.S_IROTH

'''
for root, dirs, files in os.walk(''):
  for momo in dirs:
    os.chmod(momo, allState)
  for file in files:
     fname = os.path.join(root, file)
     os.chmod(fname, allState)
'''

for dir in dirs:
    if os.path.isdir(dir):
        dirList.append(dir)
for dir in dirList:
    os.chmod(dir, allState)
    # files
    for dirF in os.listdir(dir):
        os.chmod(dir+'/'+dirF, allState)
