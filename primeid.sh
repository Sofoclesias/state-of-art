#!/bin/bash

# Check if the user has passed a number as an argument
if [ $# -eq 0 ]; then
    echo "No arguments provided. Please provide a numeric argument."
    exit 1
fi

# Number of processes to run
num_processes=$1

if ! [[ "$num_processes" =~ ^[0-9]+$ ]]; then
    echo "Error: The argument must be a valid numeric value."
    exit 1
fi

rm -rf data/

mkdir -p data/{logs,proxies,configs,ids,full}

for ((i=0; i<$num_processes; i++)); do
    kitty -e bash -c "source .venv/bin/activate && python3 primeid.py ${i} ${num_processes}" &
done

wait

cat data/ids/paperIds_*.txt > data/full/ids.txt 
rm -rf data/ids
echo "Done retrieving all. Well done."

exit