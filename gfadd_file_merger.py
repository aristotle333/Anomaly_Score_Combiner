import pandas as pd
import time
import sys

def extract_data(filename):
    file = "GFADD/gfadd/plot" + str(filename) + ".txt_10nn_32g_resultScore.txt"
    data = pd.read_csv(file, sep='\t', skipinitialspace=True, escapechar="\\", header=None)

    arr = [None] * len(data)
    for (nodeid, score) in zip(data[2],data[5]):
        arr[nodeid - 1] = score
    return arr

def write_scores_to_file(scores, filename):
    num_scores = len(scores[0])

    # Write Normalized LOF and ABOD scores to a file
    gfadd_file = open(filename, 'w')

    for node_idx in range(num_scores):
        gfadd_data_string = ""
        for plot_num in range(len(scores)):
            if plot_num == (len(scores) - 1):
                gfadd_data_string += str(scores[plot_num][node_idx]) + "\n"
            else:
                gfadd_data_string += str(scores[plot_num][node_idx]) + ","
        gfadd_file.write(gfadd_data_string)

    gfadd_file.close()

def main():
    gfadd_scores = []
    for i in range(9):
        gfadd_scores.append(extract_data(i))
    
    filename = "GFADD_scores.csv"
    write_scores_to_file(gfadd_scores, filename)

if __name__ == '__main__':
    start_time = time.time()
    main()
    print "Done, total running time was:", (time.time()-start_time), "seconds"