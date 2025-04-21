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

mkdir -p {logs,proxies,ids,full}

for ((i=0; i<$num_processes; i++)); do
    xfce4-terminal --hold --command="python3 primeid.py '${i}' '${num_processes}'"
done

wait

cat ids/paperIds_*.txt > full/ids.txt && rm -rf ids/
echo "Done retrieving all. Well done."

exit