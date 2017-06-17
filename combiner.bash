#!/bin/bash

# logfile=output.log
# exec > $logfile 2>&1
echo "Started combiner script"

# Change the inputFile path accordingly to the file you desire
inputFile="InputData/combined_data_800.csv"

echo "Creating gfadd_input_files..."
python gfadd_file_creator.py $inputFile
echo "Finished creating gfadd_input_files"

echo "Calculating GFADD scores..."
cd  GFADD
time(
for i in {0..8}
do
    make demo DATADIRS="plot"$i".txt"
done)
cd ..
echo "Finished calculating GFADD scores"

echo "Combining calculated GFADD scores in one file"
python gfadd_file_merger.py
echo "Finished combining GFADD scores in one file"

echo "Calculating abod_scores..."
python abod_score_calculation.py $inputFile
echo "Finished calculating abod_scores"

echo "Combining GFADD and ABOD scores..."
python score_combiner.py
echo "Finished combining GFADD and ABOD scores"

echo -e "\n\nTotal running time of the whole procedure was: " $SECONDS "seconds"