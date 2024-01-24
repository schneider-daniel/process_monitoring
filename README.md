# Process Metrics Recorder

This Python script monitors and records various performance metrics of a specified process using the `psutil` library. The collected metrics include CPU usage, memory percentages, RSS (Resident Set Size), and VIRT (Virtual Memory Size). The script runs for a specified duration with a given sampling frequency and outputs the data to a CSV file.

## Usage

1. **Clone the Repository:**
   ```
   git clone https://github.com/schneider-daniel/process_monitoring.git 
   cd process_monitoring
   ```
2. **Install Dependencies:**
   ```
   python3 -m pip install psutil
   ```
3. **Run the script**
   ```
   python3 record_process.py <PID> --duration <duration_seconds> --frequency <sampling_frequency> --output_file <output_file_name>
   ```

## Command-line Arguments
   ```
   - pid (int): Process ID to monitor
   - --duration (int): Duration of monitoring in seconds (default: 30)
   - --frequency (int): Sampling frequency in Hertz (default: 10)
   - --output_file (str): Name of the CSV file to store the collected metrics (default: 'process_metrics.csv')
   ```

## Example:
```
python record_process.py 1234 --duration 10 --frequency 10 --output_file process_metrics.csv

```