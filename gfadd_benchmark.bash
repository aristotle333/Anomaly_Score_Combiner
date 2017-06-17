#!/bin/bash

echo "Started combiner script"

# Change the inputFile path accordingly to the file you desire
inputFile="InputData/combined_data_full.csv"

echo "Creating gfadd_input_files..."
python gfadd_file_creator.py $inputFile
echo "Finished creating gfadd_input_files"

echo "Calculating GFADD scores..."
cd  GFADD
time(
for i in {0..7}
do
    make demo DATADIRS="plot"$i".txt" GRID=4
done)
cd ..
echo "Finished calculating GFADD scores"