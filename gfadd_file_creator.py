import pandas as pd
import time
import sys
import os

from lof import LOF
from abod import get_ABOD_scores
from numpy import mean, std, sqrt
from math import erf, log

from multiprocessing import Process, Queue

def create_gfadd_input_file(data, filename):
    path = "GFADD"
    # if not os.path.exists(path):
    #     os.makedirs(path)

    file = open(os.path.join(path, filename), 'w')

    for i in range(len(data)):
        file.write(str(i) + '\t' + str(data[i][0]) + '\t' + str(data[i][1]) + '\n')
    file.close()

def get_plot_instances(data):
    plot_instances = []
    temp_instance = []
    # degree vs. count
    for (x, y) in zip(data[0],data[1]):
        temp_instance.append([x, y])
    plot_instances.append(temp_instance)
    create_gfadd_input_file(temp_instance, "plot0.txt")

    temp_instance = []
    # pagerank_t vs. degree
    for (x, y) in zip(data[0],data[2]):
        temp_instance.append([x, y])
    plot_instances.append(temp_instance)
    create_gfadd_input_file(temp_instance, "plot1.txt")

    temp_instance = []
    # pagerank_t vs. pagerank_t_count
    for (x, y) in zip(data[2],data[3]):
        temp_instance.append([x, y])
    plot_instances.append(temp_instance)
    create_gfadd_input_file(temp_instance, "plot2.txt")

    # TODO: Change this to calculate the LOF scores for all combinations of eigenvectors,
    # currently it only uses v1 vs. v2, v3 vs. v4, v5 vs. v6, v7 vs v8, v9 vs. v10
    for i in range(5):
        temp_instance = []
        for (x, y) in zip(data[i*2 + 4],data[i*2 + 5]):
            temp_instance.append([x, y])
        plot_instances.append(temp_instance)
        create_gfadd_input_file(temp_instance, "plot"+str(i+3)+".txt")

def main(filename):
    # Read the data
    print "Filename is:", filename
    file = filename
    data = pd.read_csv(file, skipinitialspace=True, escapechar="\\", header=None)

    # Get the x,y pairs of data for each plot
    get_plot_instances(data)

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv[1])
    print "Done, creating GFADD input data, elapsed time was:", (time.time()-start_time), "seconds"
