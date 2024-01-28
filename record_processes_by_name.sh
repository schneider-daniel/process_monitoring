#!/bin/bash

# Check if process name is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <process_name>"
    exit 1
fi

# Extract process name from command-line argument
process_name="$1"

# Output file
output_file="${process_name}_top_capture.csv"

# Header
header="PID PR NI %CPU VIRT RES SHR %MEM ZEIT+ BEFEHL nTH P ZEIT SWAP CODE DATEN nMaj nMin nDRT WCHAN OOMa OOMs vMj vMn USED RSan RSfd RSlk RSsh"

# Add header to the file
echo "$header" > "$output_file"

# Find all PIDs associated with the given process name
pids=$(pgrep -f "$process_name")

# Check if any PIDs are found
if [ -z "$pids" ]; then
    echo "No processes found with name $process_name"
    exit 1
fi

# Run top in batch mode for each PID, capturing the required information
for pid in $pids; do
    top -b -n 10 -p "$pid" -d 1 | awk -v pid="$pid" '/^ *'$pid' / {print $0}' >> "$output_file"
done

echo "Capture complete. Output saved to $output_file"

