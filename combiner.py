import pandas as pd

from lof import LOF
from abod import get_ABOD_scores
from numpy import mean, std, sqrt
from math import erf

file = "combined_data_short.csv"

data = pd.read_csv(file, skipinitialspace=True, escapechar="\\", header=None)

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
    # currently it only uses v1 vs. v2, v3 vs. v4 and v5 vs. v6
    for i in range(3):
        temp_instance = []
        for (x, y) in zip(data[i*2 + 4],data[i*2 + 5]):
            temp_instance.append([x, y])
        plot_instances.append(temp_instance)

    return plot_instances

# Returns the normalized LOF and ABOD scores for all plot instances
def get_scores(plot_instances):
    lof_scores = []
    abod_scores = []

    # Generate the LOF and ABOD scores for each point in each plot
    for instance in plot_instances:
        # Calculate LOF Scores
        lof = LOF(instance)
        lof_scores_in_this_plot = []
        for point in instance:
            value = lof.local_outlier_factor(5, point)
            lof_scores_in_this_plot.append(value)
        lof_scores.append(lof_scores_in_this_plot)

        # Calculate ABOD scores
        abod_scores_in_this_plot = get_ABOD_scores(instance)
        abod_scores.append(abod_scores_in_this_plot)
        print("Finished calculating ABOD and LOF scores for a plot")

    print "Finished creating ABOD and LOF Scores"

    print "Normalizing LOF scores..."
    normalize_scores(lof_scores)
    print "Finished Normalizing LOF scores"

    print "Normalizing ABOD scores..."
    normalize_scores(abod_scores)
    print "Finished Normalizing ABOD scores"

    return lof_scores, abod_scores

def normalize_scores(scores):
    for i in range(len(scores)):
        mn = mean(scores[i])
        st_div = std(scores[i])
        for j in range(len(scores[i])):
            scores[i][j] = max(0, erf((scores[i][j] - mn) / (sqrt(2)*st_div)))


plot_instances = get_plot_instances(data)
print("Created Plot Instances")

lof_scores, abod_scores = get_scores(plot_instances)

print lof_scores, abod_scores

# # Generate the LOF and ABOD scores for each point in each plot
# for instance in plot_instances:
#     # Calculate LOF Scores
#     lof = LOF(instance)
#     lof_scores_in_this_plot = []
#     for point in instance:
#         value = lof.local_outlier_factor(5, point)
#         lof_scores_in_this_plot.append(value)
#     lof_scores.append(lof_scores_in_this_plot)

#     # Calculate ABOD scores
#     abod_scores_in_this_plot = get_ABOD_scores(instance)
#     abod_scores.append(abod_scores_in_this_plot)
#     print("Finished calculating ABOD and LOF scores for a plot")

# print("Starting LOF score normalization")
# normalize_scores(lof_scores)
# print("Finished normalizing scores")

# Write Normalized LOF and ABOD scores to a file
# lof_file = open('LOF_scores.csv', 'w')
# abod_file = open('ABOD_scores.csv', 'w')

# for i in range

# for p1, p2, p3, p4, p5, p6 in zip(lof_scores[0], lof_scores[1], lof_scores[2], lof_scores[3], lof_scores[4], lof_scores[5]):
#     f.write(str(p1)+","+str(p2)+","+str(p3)+","+str(p4)+","+str(p5)+","+str(p6)+"\n")

# f.close()
# print("Done")