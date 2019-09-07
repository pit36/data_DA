import csv
import matplotlib.pyplot as plt
import argparse


parser = argparse.ArgumentParser(description='Plotting Average Latency')
parser.add_argument('--load_level', default= 0, type=int, help='Set if there are different load levels, 1 is with changing load levels')
args = parser.parse_args()

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
with open('average_latency.csv') as csvfile:
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
            print('text')
            print(verticalLine[0])
            plt.text(verticalLine[0] + 1, 110, s=str(verticalLine[1]), rotation=90)
        else:
            plt.text(verticalLine[0] + 1, 110, s='End', rotation=90)

plt.plot(stepList, rewardList)

plt.xlabel('Steps')
plt.ylabel('Average Latency (ms)')
#plt.savefig('avg_lat.pdf')

plt.show()