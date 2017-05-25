# Anomaly Score Combiner

## Instructions
To execute type: `python combiner.py`

Running the above command will read the plot data and create two files named `ABOD_scores.csv`
and `LOF_scores.csv` that will contain the normalized scores for each point in each plot.

The ABOD scores have undergone logarithmic inversion so that a small ABOD score means that it
is less likely to be a outlier.

Finally the scores for each point in each plot are combined to form the combined scores of each
node that are written to the `combined_scores.csv` file.

The weights used for combining are currently `1` for plots 1-3 and `1/3` for plots 4-6

## Credits

LOF scores are calculated using the implementation found [here](https://github.com/damjankuznar/pylof/blob/master/lof.py)

ABOD scores are calculated using a modified version of the implementation found here: [here](https://github.com/MarinYoung4596/OutlierDetection/blob/master/OutlierDetection/Python%20Implementation/abod.py)