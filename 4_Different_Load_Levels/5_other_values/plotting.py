import csv
import matplotlib.pyplot as plt
import argparse
import os
import numpy as np
import math

parser = argparse.ArgumentParser(description='Plotting Reward')

parser.add_argument('--file', default=0, type=int, help='0  if average, 1 if reward')
args = parser.parse_args()
filename = "average_latency.csv"
if args.file == 1:
    filename = "reward_controller.csv"


# check how many folders
dataDict = {}
plt.figure()

dirList = []
onlyDir = []
folder = ['softmax']
steps = 30
for fld in folder:
    dirsss = os.listdir(fld)
    dirs = []
    for dir in dirsss:
        if os.path.isdir(fld +'/'+dir):
            dirs.append(dir)
    print(dirs)
    for it in dirs:
        dirss = os.listdir(fld +'/'+it)
        # folderStr = fld + '/' + dirss
        for dir in dirss:
            dirStr = fld + '/' + it + '/' + dir
            if os.path.isdir(dirStr):
                dirList.append(dirStr)
                onlyDir.append(dir)
        dataList = []
        dataDict[fld] = {}
        for dir in dirList:
            load_level = onlyDir[dirList.index(dir)]
            if dir not in dataDict[fld]:
                dataDict[fld][load_level] = []
            rewardList = []
            stepList = []
            # read out reward
            with open('{}/{}'.format(dir, filename)) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                rowIterator = 0
                for row in reader:
                    if '#' not in row[0]:
                        if int(row[0]) < 50000 and int(row[0]) > 150:
                            rewardList.append(float(row[1]))
                            stepList.append(int(row[0]))
                        #else:
                        #    break
            dataDict[fld][load_level] = dataDict[fld][load_level] + rewardList

print(dataDict)
dataReordered = {}
for key in dataDict:
    dataReordered[key] = {}
    for dir in dataDict[key]:
        rewardList = dataDict[key][dir]
        if len(rewardList) > 0:
            #if key == 'Q_L':
            #    print(rewardList)
            avgReward = np.average(rewardList)
            up = np.percentile(rewardList, 95)
            down = np.percentile(rewardList, 5)
            dataReordered[key][dir] = (avgReward, up, down)
dataDictKeys = {}
for key in dataReordered:
    x = []
    y = []
    plotty = []
    yerrup = []
    yerrdown = []
    for dir in dataReordered[key]:
        dirFloat = float(dir)
        plotty.append([dirFloat, dataReordered[key][dir][0], dataReordered[key][dir][1], dataReordered[key][dir][2]])
    sortedPlottly = sorted(plotty)
    for plottyy in sortedPlottly:
        x.append(plottyy[0]*10.0)
        y.append(plottyy[1])
        yerrup.append(plottyy[2])
        yerrdown.append(plottyy[3])
    #plt.plot(x, y, label='{}'.format(key))
    plt.errorbar(x, y,
            yerr=[np.subtract(y, yerrdown), np.subtract(yerrup, y)],
            fmt='-', label=key)
    #plt.fill_between(x, yerrup, yerrdown, alpha=.2)

plt.xlabel('Load Level (%)')
label = 'Average Latency'
if args.file == 1:
    label = 'Reward'
plt.ylabel(label)
plt.savefig('LL.pdf')
plt.legend(loc='lower right')
plt.show()
