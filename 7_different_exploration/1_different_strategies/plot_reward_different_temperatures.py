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

plt.figure()

dirList = []
folder = ['Softmax/1','Softmax/2','Softmax/3','Softmax/5', 'Softmax/10', 'Softmax/20', 'eps_greedy/0.1','eps_greedy/0.2','eps_greedy/0.3']
load = '10'
steps = 30
for fld in folder:
    print(fld)
    dirss = os.listdir(fld)
    # folderStr = fld + '/' + dirss
    for dir in dirss:
        dirStr = fld + '/' + dir
        if os.path.isdir(dirStr):
            dirList.append(dirStr)
    dataList = []
    for dir in dirList:
        rewardList = []
        stepList = []

        # read out reward
        with open('{}/{}/average_latency.csv'.format(dir, load)) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            rowIterator = 0
            for row in reader:
                if '#' not in row[0]:
                    if int(row[0]) < 50000:
                        rewardList.append(float(row[1]))
                        stepList.append(int(row[0]))
        dataList.append((stepList, rewardList))
    average = args.average
    lowest = math.inf
    highest = 0
    # find the lowest value
    for data in dataList:
        if lowest > len(data[0]):
            lowest = len(data[0])
        if highest < len(data[0]):
            highest = len(data[0])
    steps = int(lowest // average)
    dataPointList = {}
    for step in range(0, steps):
        lowBorder = step * average
        highBorder = (step + 1) * average
        dataPointList[step] = []
        for data in dataList:
            dataArray = []
            #for x in range(lowBorder, highBorder):
            if step < len(data[1]):
                dataArray.append(data[1][lowBorder])
            dataPointList[step].append(np.average(dataArray))

    x = []
    y = []
    yerr = []
    yerrup = []
    yerrdown = []
    for dataPoint in dataPointList:
        avg = np.average(dataPointList[dataPoint])
        #avg = np.percentile(dataPointList[dataPoint], 50)
        up = np.percentile(dataPointList[dataPoint], 95)
        down = np.percentile(dataPointList[dataPoint], 5)
        # std = np.std(dataPointList[dataPoint])
        # yerr.append(std)
        yerrup.append(up)
        yerrdown.append(down)
        y.append(avg)
        x.append(dataPoint)

    x = x[:steps]
    y = y[:steps]
    yerrup = yerrup[:steps]
    yerrdown = yerrdown[:steps]
    print("Highest: {}, lowest: {}".format(highest, lowest))
    plt.plot(x, y, label='{}'.format(fld))
    #plt.fill_between(x, yerrup, yerrdown, alpha=.2)

plt.xlabel('Steps')
plt.ylabel('Average Latency')
plt.legend(loc='lower right')
plt.savefig('Average_Latency.pdf')
plt.show()
