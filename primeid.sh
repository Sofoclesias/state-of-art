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

mkdir -p data/{logs,templog,proxies,tempid} data/proxies/{configs,errors,logs}

for ((i=0; i<$num_processes; i++)); do
    touch "data/proxies/HEALTH_${i}_0"
    kitty -e bash -c "source .venv/bin/activate && python3 primeid.py ${i} ${num_processes}" &
done

wait

cat data/tempid/paperIds_*.txt > data/ids_$(date +%d%m%Y).txt 
cat data/templog/delays_*.txt > data/logs/delays_$(date +%d%m%Y).txt
cat data/templog/connections_*.txt > data/logs/connections_$(date +%d%m%Y).txt
rm -rf data/{templog,proxies,tempid}

echo "Done retrieving all. Well done."

exit