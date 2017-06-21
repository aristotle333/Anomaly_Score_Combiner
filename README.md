# Anomaly Score Combiner

## Instructions

### Calculating both ABOD and GFADD scores
Modify the `inputFile` variable in the `combiner.bash` so that it specifices the input data for
which you want to calculate ABOD and GFADD scores.

To execute type: `./combiner.bash`

Running the above command will read the plot data and create two files named `ABOD_scores.csv`
and `GFADD_scores.csv` that will contain the normalized scores for each point in each plot.

The ABOD scores have undergone logarithmic inversion so that a small ABOD score means that it
is less likely to be a outlier.

Finally the scores for each point in each plot are combined to form the combined scores of each
node that are written to the `combined_scores.csv` file.

The weights used for combining are currently `1` for plots 1-4 and `1/5` for plots 5-9

### GFADD scores only
Because calculating ABOD scores is slow you may only want to calculate the GFADD scores.
To do that just run the `combiner_gfadd.bash` script. Modify the `inputFile` variable to the
desired input file in the same way as before. Running the `combiner_gfadd.bash` script will create
both `GFADD_scores.csv` and `combined_scores.csv` files but they will be identical.

## Credits

ABOD scores are calculated using a modified version of the implementation found here: [here](https://github.com/MarinYoung4596/OutlierDetection/blob/master/OutlierDetection/Python%20Implementation/abod.py)