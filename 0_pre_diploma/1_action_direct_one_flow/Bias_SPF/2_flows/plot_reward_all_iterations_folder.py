import csv
import matplotlib.pyplot as plt
import argparse
import os
import numpy as np
import math
parser = argparse.ArgumentParser(description='Plotting Reward')
parser.add_argument('--load_level', default= 0, type=int, help = 'Set if there are different load levels, 1 is with changing load levels')
parser.add_argument('--average', default= 1, type=int, help = 'How many datapoints should be plotted as an average')
args = parser.parse_args()
# check how many folders

plt.figure()

dirList= []
folder = ['direct', 'one_flow']

for fld in folder:
	print(fld)
	dirss = os.listdir(fld)
	#folderStr = fld + '/' + dirss
	for dir in dirss:
		dirStr = fld + '/' + dir
		print("Dir: {}".format(dirStr))
		if os.path.isdir(dirStr):
		    dirList.append(dirStr)
	print(dirList)
	dataList = []
	for dir in dirList:

		if args.load_level:
		    # read Out Mininet
		    mininetTimeStampLoadList = []
		    mininetLoadList = []
		    with open('timestamp_changing_load_levels_mininet.csv') as csvfile:
		        reader = csv.reader(csvfile, delimiter= ',')
		        for row in reader:
		            if '#' not in row[0]:
		                mininetTimeStampLoadList.append(row[1])
		                mininetLoadList.append(row[0])
		    timeStampRowIterator = 0
		    verticalLineList = []

		rewardList = []
		stepList = []

		# read out reward
		with open('{}/reward_controller.csv'.format(dir)) as csvfile:
		    reader = csv.reader(csvfile, delimiter= ',')
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

		if args.load_level:
		    print(verticalLineList)
		    for verticalLine in verticalLineList:
		        plt.axvline(verticalLine[0], color='g')
		        if(int(verticalLine[1]) > 1):
		            plt.text(verticalLine[0] + 1, -13, s=str(verticalLine[1]), rotation=90)
		        else:
		            plt.text(verticalLine[0] + 1, -13, s='End', rotation=90)
		dataList.append((stepList, rewardList))
	average = args.average
	if not args.load_level:
		print(dataList)
		lowest = math.inf
		for data in dataList:
		    if lowest > len(data[0]):
		        lowest = len(data[0])
		steps = lowest // average
		dataPointList = {}
		for step in range(0, steps):
		    lowBorder = step * average
		    highBorder = (step+1) * average
		    dataPointList[step] = []
		    for data in dataList:
		        dataArray = []
		        for x in range(lowBorder, highBorder):
		            dataArray.append(data[1][x])
		        dataPointList[step].append(np.average(dataArray))
		print(dataPointList)

	x = []
	y = []
	yerr = []
	yerrup = []
	yerrdown = []
	for dataPoint in dataPointList:
		avg = np.average(dataPointList[dataPoint])
		std = np.std(dataPointList[dataPoint])
		yerr.append(std)
		yerrup.append(avg + std)
		yerrdown.append(avg - std)
		y.append(avg)
		x.append(dataPoint)

	steps = 30
	x = x[:steps]
	y = y[:steps]
	yerrup = yerrup[:steps]
	yerrdown = yerrdown[:steps]

	plt.plot(x, y)
	plt.fill_between(x, yerrup, yerrdown, alpha=.2)

plt.xlabel('Steps')
plt.ylabel('Average Reward')
plt.savefig('Average_Reward.pdf')

plt.show()
