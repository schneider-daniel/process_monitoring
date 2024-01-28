#!/bin/bash

# Check if PID is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <PID>"
    exit 1
fi

# Extract PID from command-line argument
pid="$1"

# Output file
output_file="pid${pid}_top_capture.csv"

# Header
header="PID PR NI %CPU VIRT RES SHR %MEM ZEIT+ BEFEHL nTH P ZEIT SWAP CODE DATEN nMaj nMin nDRT WCHAN OOMa OOMs vMj vMn USED RSan RSfd RSlk RSsh"

# Add header to the file
echo "$header" > "$output_file"

# Run top in batch mode, capturing the required information
top -b -n 10 -p "$pid" -d 1 | awk -v pid="$pid" '/^ *'$pid' / {print $0}' >> "$output_file"

echo "Capture complete. Output saved to $output_file"

