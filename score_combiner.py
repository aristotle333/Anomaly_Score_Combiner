import pandas as pd
import time
import sys

from numpy import mean, std, sqrt
from math import erf, log

# Perform score combination to get a final outlier score for each node
def form_combined_scores(gfadd_scores_filename, abod_scores_filename, combined_scores_filename):
    start_time = time.time()
    print "Reading scores data from " + gfadd_scores_filename, abod_scores_filename
    # Weights for each plot from 1-8 respectively
    weights = [1, 1, 1, 1/3 ,1/3 ,1/3, 1/3, 1/3]

    gfadd_scores_data = pd.read_csv(gfadd_scores_filename, skipinitialspace=True, escapechar="\\", header=None)
    abod_scores_data = pd.read_csv(abod_scores_filename, skipinitialspace=True, escapechar="\\", header=None)

    scores = [gfadd_scores_data, abod_scores_data]

    num_scores = len(gfadd_scores_data[0])

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

    print "Writting combined scores data to " + combined_scores_filename 
    combined_scores_file = open(combined_scores_filename, 'w')
    for score in combined_scores:
        combined_scores_file.write(str(score) + "\n")
    combined_scores_file.close()
    print "Finished writting combined scores to " + combined_scores_filename
    print "Time to combine all scores and write them to a file was: " + str(time.time()-start_time) + " seconds"

def main():
    gfadd_scores_filename = "GFADD_scores.csv"
    abod_scores_filename = "ABOD_scores.csv"
    combined_scores_filename = "combined_scores.csv"

    form_combined_scores(gfadd_scores_filename, abod_scores_filename, combined_scores_filename)

if __name__ == '__main__':
    start_time = time.time()
    main()
    print "Done, total running time was:", (time.time()-start_time), "seconds"