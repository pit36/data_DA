import csv
import matplotlib.pyplot as plt
import argparse
import os
import numpy as np
import math

parser = argparse.ArgumentParser(description='Plotting Reward')
parser.add_argument('--load_level', default=0, type=int,
                    help='Set if there are different load levels, 1 is with changing load levels')
parser.add_argument('--average', default=1, type=int, help='How many datapoints should be plotted as an average')
args = parser.parse_args()
# check how many folders
dataDict = {}
plt.figure()

dirList = []
onlyDir = []
folder = ['Learning', 'SPF']
steps = 30
for fld in folder:
    print(fld)
    dirss = os.listdir(fld)
    # folderStr = fld + '/' + dirss
    for dir in dirss:
        dirStr = fld + '/' + dir
        if os.path.isdir(dirStr):
            dirList.append(dirStr)
            onlyDir.append(dir)
    dataList = []
    dataDict[fld] = {}
    for dir in dirList:

        rewardList = []
        stepList = []
        # read out reward
        with open('{}/average_latency.csv'.format(dir)) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            rowIterator = 0
            for row in reader:
                if '#' not in row[0]:
                    if int(row[0]) < 5000:
                        rewardList.append(float(row[1]))
                        stepList.append(int(row[0]))
                        if args.load_level:
                            time = row[2]
                            if timeStampRowIterator < len(mininetLoadList):
                                if time > mininetTimeStampLoadList[timeStampRowIterator]:
                                    verticalLineList.append((int(row[0]), mininetLoadList[timeStampRowIterator]))
                                    timeStampRowIterator += 1
                                rowIterator += 1
                    else:
                        break
        dataDict[fld][onlyDir[dirList.index(dir)]] = [stepList, rewardList]
plotDick = {}
for key in dataDict:
    plotDick[key] = {}
    for dir in dataDict[key]:
        rewardList = dataDict[key][dir][1]
        avgReward = np.average(rewardList)
        up = np.percentile(rewardList, 95)
        down = np.percentile(rewardList, 5)
        plotDick[key][dir] = (avgReward, up, down)
print(plotDick)
dataDictKeys = {}
for key in plotDick:
    x = []
    y= []
    plotty = []
    yerrup = []
    yerrdown = []
    for dir in plotDick[key]:
        dirFloat = float(dir)
        plotty.append([dirFloat, plotDick[key][dir][0], plotDick[key][dir][1], plotDick[key][dir][2]])
        #.append(dirFloat,)
        #yerrup.append(plotDick[key][dir][1])
        #yerrdown.append(plotDick[key][dir][2])
    sortedPlottly = sorted(plotty)
    for plottyy in sortedPlottly:
        x.append(plottyy[0])
        y.append(plottyy[1])
        yerrup.append(plottyy[2])
        yerrdown.append(plottyy[3])
    #plt.plot(x, y, label='{}'.format(key))
    plt.errorbar(x, y,
            yerr=[np.subtract(yerrup, y), np.subtract(y, yerrdown)],
            fmt='-', label='fld')
    #plt.fill_between(x, yerrup, yerrdown, alpha=.2)

plt.xlabel('Load Level')
plt.ylabel('Latency')
plt.savefig('LL.pdf')
plt.legend(loc='lower right')
plt.show()