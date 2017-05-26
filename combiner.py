import pandas as pd
import time

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
    for point in instance:
        value = lof.local_outlier_factor(5, point)
        lof_scores_in_this_plot.append(value)
    dictionary = {plot_num: lof_scores_in_this_plot} 
    lof_queue.put(dictionary)
    print "Finished calculating LOF scores for plot", plot_num, "elapsed time:", time.time() - start_time

def calculate_abod_scores(instance, plot_num, abod_queue):
    print "Started calculating ABOD scores for plot", plot_num
    start_time = time.time()
    abod_scores_in_this_plot = get_ABOD_scores(instance)
    dictionary = {plot_num: abod_scores_in_this_plot} 
    abod_queue.put(dictionary)
    print "Finished calculating ABOD scores for plot", plot_num, "elapsed time:", time.time() - start_time

# Returns the normalized LOF and ABOD scores for all plot instances
def get_scores(plot_instances):
    start_time = time.time()
    num_plots = len(plot_instances)
    lof_scores = [None] * num_plots
    abod_scores = [None] * num_plots

    lof_time = 0
    abod_time = 0

    # Variables used for multiprocessing purposes
    plot_num = 0
    lof_queue = Queue()
    abod_queue = Queue()
    lof_processes = []
    abod_processes = []

    get_scores_time = time.time()

    # Generate the LOF and ABOD scores for each point in each plot using multiproccessing
    for instance in plot_instances:
        lof_process = Process(target=calculate_lof_scores,args=(instance, plot_num, lof_queue))
        lof_process.start()
        lof_processes.append(lof_process)

        abod_process = Process(target=calculate_abod_scores,args=(instance, plot_num, abod_queue))
        abod_process.start()
        abod_processes.append(abod_process)
        plot_num += 1

        # lof_start_time = time.time()
        # # Calculate LOF Scores
        # lof = LOF(instance)
        # lof_scores_in_this_plot = []
        # for point in instance:
        #     value = lof.local_outlier_factor(5, point)
        #     lof_scores_in_this_plot.append(value)
        # lof_scores.append(lof_scores_in_this_plot)
        # lof_time += (time.time() - lof_start_time)
        # print "Elapsed time for LOF scores so far is:", lof_time, "seconds"

        # abod_start_time = time.time()
        # # Calculate ABOD scores
        # abod_scores_in_this_plot = get_ABOD_scores(instance)
        # abod_scores.append(abod_scores_in_this_plot)
        # abod_time += (time.time() - abod_start_time)
        # print "Elapsed time for ABOD scores so far is:", abod_time, "seconds"
        # print "Finished calculating ABOD and LOF scores for a plot", plot_num

    lof_results = {}
    abod_results = {}

    for i in range(num_plots):
        lof_results.update(lof_queue.get())

    for i in range(num_plots):
        abod_results.update(abod_queue.get())

    for proc in lof_processes:
        proc.join()

    for proc in abod_processes:
        proc.join()

    for key, val in lof_results.iteritems():
        lof_scores[key] = val

    for key, val in abod_results.iteritems():
        abod_scores[key] = val

    print "Finished creating ABOD and LOF Scores, elapsed time is:", time.time() - get_scores_time

    norm_lof_scores_time = time.time()
    print "Normalizing LOF scores..."
    normalize_scores(lof_scores)
    lof_time += (time.time() - norm_lof_scores_time)
    print "Finished Normalizing LOF scores in " + str(time.time()-norm_lof_scores_time) + " seconds"

    norm_abod_scores_time = time.time()
    print "Performing Logarithmic Inversion on ABOD scores..."
    score_logarithmic_inversion(abod_scores)
    print "Finished Logarithmic Iversion for ABOD scores"

    print "Normalizing ABOD scores..."
    normalize_scores(abod_scores)
    abod_time += (time.time() - norm_abod_scores_time)
    print "Finished Normalizing ABOD scores in " + str(time.time()-norm_abod_scores_time) + " seconds"

    print "Total time calculating and normalizing LOF scores was", lof_time, "seconds"
    print "Total time calculating and normalizing ABOD scores was", abod_time, "seconds"
    print "Time taken to calculte all ABOD and LOF scores with normalization was " + str(time.time() - start_time) + " seconds"
    return lof_scores, abod_scores

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

def write_scores_to_file(lof_scores, abod_scores, lof_scores_filename, abod_scores_filename, plot_instances):
    num_scores = len(plot_instances[0])

    # Write Normalized LOF and ABOD scores to a file
    lof_file = open(lof_scores_filename, 'w')
    abod_file = open(abod_scores_filename, 'w')

    for node_idx in range(num_scores):
        lof_data_string = ""
        abod_data_string = ""
        for plot_num in range(len(plot_instances)):
            if plot_num == (len(plot_instances) - 1):
                lof_data_string += str(lof_scores[plot_num][node_idx]) + "\n"
                abod_data_string += str(abod_scores[plot_num][node_idx]) + "\n"
            else:
                lof_data_string += str(lof_scores[plot_num][node_idx]) + ","
                abod_data_string += str(abod_scores[plot_num][node_idx]) + ","
        lof_file.write(lof_data_string)
        abod_file.write(abod_data_string)

    lof_file.close()
    abod_file.close()

# Perform score combination to get a final outlier score for each node
def form_combined_scores(lof_scores_filename, abod_scores_filename, combined_scores_filename):
    start_time = time.time()
    print "Reading scores data from " + lof_scores_filename, abod_scores_filename
    # Weights for each plot from 1-8 respectively
    weights = [1, 1, 1, 1/3 ,1/3 ,1/3, 1/3, 1/3]

    lof_scores_data = pd.read_csv(lof_scores_filename, skipinitialspace=True, escapechar="\\", header=None)
    abod_scores_data = pd.read_csv(abod_scores_filename, skipinitialspace=True, escapechar="\\", header=None)

    scores = [lof_scores_data, abod_scores_data]

    num_scores = len(lof_scores_data[0])

    print("Combining scores data ...")
    combined_scores = []
    for i in range(num_scores):
        numerator = 0
        denominator = 0
        for plot_num in range(8):
            for score in scores:
                numerator += (weights[plot_num] * score[plot_num][i])
                denominator += weights[plot_num]

        combined_scores.append(numerator/denominator)

    print "Done combining scores data"

    print "Writting combined scores data to " + abod_scores_filename 
    combined_scores_file = open(combined_scores_filename, 'w')
    for score in combined_scores:
        combined_scores_file.write(str(score) + "\n")
    combined_scores_file.close()
    print "Finished writting combined scores to " + abod_scores_filename
    print "Time to combine all scores and write them to a file was: " + str(time.time()-start_time) + " seconds"

def main():
    # Read the data
    file = "InputData/combined_data_short.csv"
    data = pd.read_csv(file, skipinitialspace=True, escapechar="\\", header=None)

    # Get the x,y pairs of data for each plot
    plot_instances = get_plot_instances(data)
    print "Created Plot Instances"

    lof_scores, abod_scores = get_scores(plot_instances)

    lof_scores_filename = "LOF_scores.csv"
    abod_scores_filename = "ABOD_scores.csv"
    combined_scores_filename = "combined_scores.csv"

    write_scores_to_file(lof_scores, abod_scores, lof_scores_filename, abod_scores_filename, plot_instances)

    form_combined_scores(lof_scores_filename, abod_scores_filename, combined_scores_filename)

if __name__ == '__main__':
    start_time = time.time()
    main()
    print "Done, total running time was:", (time.time()-start_time), "seconds"
