import subprocess
import argparse
import os

parser = argparse.ArgumentParser(description='Plot average latency vs. steps for different approaches')

parser.add_argument('--folder', default="./data_NSFNET", type=str, help='Specify folder of measurements')
args = parser.parse_args()

folderpath = args.folder


def get_subdirs(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def get_logs(a_dir):
    return [name for name in os.listdir(a_dir) if os.path.isfile(os.path.join(a_dir, name))]


algos = get_subdirs(folderpath)
print(algos)
for algo in algos:
    print(folderpath + "/" + algo)
    iterations = sorted(get_logs(folderpath + "/" + algo))
    print(iterations)

    for iteration in iterations:
        c = iteration.split(".")[1]
        d = folderpath + "/" + algo + "/" + iteration.split(".")[1]
        log = folderpath + "/" + algo + "/" + iteration
        subprocess.call(
            ['mkdir {}'.format(folderpath + "/" + algo + "/" + str(c))], shell=True)
        print('tar -xf {} -C {}'.format(log, d))
        subprocess.call(
            ['tar -xf {} -C {}'.format(log, d)], shell=True)
        subprocess.call(
            ['mv {}/home/vagrant/logs/* {}'.format(d, d)], shell=True)
        subprocess.call(
            ['rm -r {}/0/'.format(d)], shell=True)
        subprocess.call(
            ['rm -r {}/home/'.format(d)], shell=True)

subprocess.call(
    ['chmod -R a+rw {}'.format(folderpath)], shell=True)
