import pandas as pd
import time
import sys

from lof import LOF
from abod import get_ABOD_scores
from numpy import mean, std, sqrt
from math import erf, log

from multiprocessing import Process, Queue

def get_plot_instances(data):
    plot_instances = []
    temp_instance = []
    # degree vs. count
    for (x, y) in zip(data[0],data[1]):
        temp_instance.append([x, y])
    plot_instances.append(temp_instance)

    temp_instance = []
    # pagerank_t vs. degree
    for (x, y) in zip(data[0],data[2]):
        temp_instance.append([x, y])
    plot_instances.append(temp_instance)

    temp_instance = []
    # pagerank_t vs. pagerank_t_count
    for (x, y) in zip(data[2],data[3]):
        temp_instance.append([x, y])
    plot_instances.append(temp_instance)

    # TODO: Change this to calculate the LOF scores for all combinations of eigenvectors,
    # currently it only uses v1 vs. v2, v3 vs. v4, v5 vs. v6, v7 vs v8, v9 vs. v10
    for i in range(5):
        temp_instance = []
        for (x, y) in zip(data[i*2 + 4],data[i*2 + 5]):
            temp_instance.append([x, y])
        plot_instances.append(temp_instance)

    return plot_instances

def calculate_lof_scores(instance, plot_num, lof_queue):
    print "Started calculating LOF scores for plot", plot_num
    start_time = time.time()
    lof = LOF(instance)
    lof_scores_in_this_plot = []
    i = 0
    for point in instance:
        if (i  + 1) % 100 == 0:
            print "Calculated", i, "LOF scores for plot", plot_num, "elapsed time is:", time.time() - start_time
        value = lof.local_outlier_factor(5, point)
        lof_scores_in_this_plot.append(value)
        i += 1
    dictionary = {plot_num: lof_scores_in_this_plot} 
    lof_queue.put(dictionary)
    print "Finished calculating LOF scores for plot", plot_num, "elapsed time:", time.time() - start_time

def calculate_abod_scores(instance, plot_num, abod_queue):
    print "Started calculating ABOD scores for plot", plot_num
    start_time = time.time()
    abod_scores_in_this_plot = get_ABOD_scores(instance, plot_num)
    dictionary = {plot_num: abod_scores_in_this_plot} 
    abod_queue.put(dictionary)
    print "Finished calculating ABOD scores for plot", plot_num, "elapsed time:", time.time() - start_time

# Returns the normalized LOF and ABOD scores for all plot instances
def get_scores(plot_instances):
    start_time = time.time()
    num_plots = len(plot_instances)
    abod_scores = [None] * num_plots

    abod_time = 0

    # Variables used for multiprocessing purposes
    plot_num = 0
    abod_queue = Queue()
    abod_processes = []

    get_scores_time = time.time()

    # Generate the ABOD scores for each point in each plot using multiproccessing
    for instance in plot_instances:
        abod_process = Process(target=calculate_abod_scores,args=(instance, plot_num, abod_queue))
        abod_process.start()
        abod_processes.append(abod_process)
        plot_num += 1

    abod_results = {}

    for i in range(num_plots):
        abod_results.update(abod_queue.get())

    for proc in abod_processes:
        proc.join()

    for key, val in abod_results.iteritems():
        abod_scores[key] = val

    print "Finished creating ABOD Scores, elapsed time is:", time.time() - get_scores_time

    norm_abod_scores_time = time.time()
    print "Performing Logarithmic Inversion on ABOD scores..."
    score_logarithmic_inversion(abod_scores)
    print "Finished Logarithmic Iversion for ABOD scores"

    print "Normalizing ABOD scores..."
    normalize_scores(abod_scores)
    abod_time += (time.time() - norm_abod_scores_time)
    print "Finished Normalizing ABOD scores in " + str(time.time()-norm_abod_scores_time) + " seconds"

    print "Total time calculating and normalizing ABOD scores was", abod_time, "seconds"
    print "Time taken to calculte all ABOD scores with normalization was " + str(time.time() - start_time) + " seconds"
    return abod_scores

def score_logarithmic_inversion(scores):
    for i in range(len(scores)):
        max_score = max(scores[i])
        for j in range(len(scores[i])):
            scores[i][j] = -log(scores[i][j] / max_score)

def normalize_scores(scores):
    for i in range(len(scores)):
        mn = mean(scores[i])
        st_div = std(scores[i])
        for j in range(len(scores[i])):
            scores[i][j] = max(0, erf((scores[i][j] - mn) / (sqrt(2)*st_div)))

def write_scores_to_file(abod_scores, abod_scores_filename, plot_instances):
    num_scores = len(plot_instances[0])

    # Write Normalized LOF and ABOD scores to a file
    abod_file = open(abod_scores_filename, 'w')

    for node_idx in range(num_scores):
        abod_data_string = ""
        for plot_num in range(len(plot_instances)):
            if plot_num == (len(plot_instances) - 1):
                abod_data_string += str(abod_scores[plot_num][node_idx]) + "\n"
            else:
                abod_data_string += str(abod_scores[plot_num][node_idx]) + ","
        abod_file.write(abod_data_string)

    abod_file.close()

def main(filename):
    # Read the data
    print "Reading input data from", filename
    file = filename
    data = pd.read_csv(file, skipinitialspace=True, escapechar="\\", header=None)

    # Get the x,y pairs of data for each plot
    plot_instances = get_plot_instances(data)
    print "Created Plot Instances"

    abod_scores = get_scores(plot_instances)

    abod_scores_filename = "ABOD_scores.csv"
    write_scores_to_file(abod_scores, abod_scores_filename, plot_instances)

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv[1])
    print "Done, total running time was:", (time.time()-start_time), "seconds"
