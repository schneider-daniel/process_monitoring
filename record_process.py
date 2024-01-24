#!/bin/python3

"""
Monitor and record performance metrics of a specified process.

This script utilizes the psutil library to monitor and record various performance
metrics of a specified process. The collected metrics include CPU usage, memory
percentages, RSS (Resident Set Size), and VIRT (Virtual Memory Size). The script
runs for a specified duration with a given sampling frequency and outputs the data
to a CSV file.

Parameters:
    pid (int): Process ID to monitor.
    duration_seconds (int): Duration of the monitoring in seconds (default: 30).
    sample_frequency_hz (int): Sampling frequency in Hertz (default: 10).
    output_file (str): Name of the CSV file to store the collected metrics
                      (default: 'process_metrics.csv').

Example:
    To monitor the process with PID 232537 for 30 seconds at a frequency of 10 Hz
    and save the metrics to 'process_metrics.csv':
    
    ```
    python record_process.py 232537 --duration 30 --frequency 10 --output_file process_metrics.csv
    ```

Note:
    - The script calculates memory percentages, RSS, and VIRT in megabytes.
    - It includes system-wide memory information such as total physical memory (RAM)
      and total swap space in the recorded metrics.
    - The output CSV file contains columns for Timestamp, Process ID (PID), CPU
      percentage, Memory percentage, RSS, and VIRT.

Command-line Arguments:
    - pid: Process ID to monitor.
    - --duration: Duration of monitoring in seconds (default: 30).
    - --frequency: Sampling frequency in Hertz (default: 10).
    - --output_file: Name of the output CSV file (default: 'process_metrics.csv').
"""

import psutil
from time import time, sleep
import csv
import argparse

def get_current_time():
    # Get current time in epoch time format with nanosecond precision
    current_time = time()
    return current_time

def record_process_metrics(pid, duration_seconds, sample_frequency_hz, output_file):
    target_freq = 1.0 / sample_frequency_hz
    total_samples = int(duration_seconds * sample_frequency_hz)

    # Get system memory information
    total_physical_memory = psutil.virtual_memory().total
    total_swap_space = psutil.swap_memory().total

    rows = []  # List to store rows

    for _ in range(total_samples):
        sample_start_time = time()

        process = psutil.Process(pid)
        cpu_percent = process.cpu_percent(interval=target_freq)  # No interval for instantaneous measurement
        mem_info = process.memory_info()
        rss = mem_info.rss / (1024 ** 2)  # Convert RSS to megabytes
        virt = mem_info.vms / (1024 ** 2)  # Convert VIRT to megabytes

        current_time = get_current_time()

        row = {
            'Timestamp': current_time,
            'PID': pid,
            'CPU%': cpu_percent,
            'Memory%': process.memory_percent(),
            'RSS': rss,
            'VIRT': virt
        }

        rows.append(row)

        sample_end_time = time()
        time_diff = sample_end_time - sample_start_time

        if time_diff < target_freq:
            sleep(target_freq - time_diff)

    # Write all rows to the CSV file at once
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Timestamp', 'PID', 'CPU%', 'Memory%', 'RSS', 'VIRT']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monitor and record performance metrics of a specified process.')
    parser.add_argument('pid', type=int, help='Process ID to monitor.')
    parser.add_argument('--duration', type=int, default=30, help='Duration of the monitoring in seconds (default: 30).')
    parser.add_argument('--frequency', type=int, default=10, help='Sampling frequency in Hertz (default: 10).')
    parser.add_argument('--output_file', default='process_metrics.csv', help='Name of the CSV file to store the collected metrics (default: process_metrics.csv).')

    args = parser.parse_args()

    record_process_metrics(args.pid, args.duration, args.frequency, args.output_file)

