#!/bin/bash

echo "Started combiner script"

# Change the inputFile path accordingly to the file you desire
inputFile="InputData/combined_data_full.csv"

echo "Creating gfadd_input_files..."
python gfadd_file_creator.py $inputFile
echo "Finished creating gfadd_input_files"

echo "Calculating GFADD scores..."
cd  GFADD
GFADD_START_TIME=$SECONDS
for i in {0..8}
do
    make demo DATADIRS="plot"$i".txt"
done
GFADD_RUNTIME=$((SECONDS-GFADD_START_TIME))
echo "Runtime of GFADD algorithm was: " $GFADD_RUNTIME "seconds"

cd ..
echo "Finished calculating GFADD scores"

echo "Combining calculated GFADD scores in one file"
python gfadd_file_merger.py
echo "Finished combining GFADD scores in one file"

echo "Combining GFADD scores..."
python gfadd_score_combiner.py
echo "Finished combining GFADD"

echo -e "\n\nTotal running time of the whole procedure was: " $SECONDS "seconds"
