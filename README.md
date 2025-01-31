# Internet Speed Monitoring

This application monitors your internet connection speed, recording:
- Download Speed (Mbps)
- Upload Speed (Mbps)
- Latency/Ping (ms)
- Jitter/Latency variation (ms)

## Requirements

- Python with pip installed
- Python packages listed in `requirements.txt`

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note**: After installing dependencies, run the setup assistant. It will guide you through the initial configuration process.
```bash
python install.py
```

## Usage

To run a speed test:
```bash
python monitor.py
```

Results will be saved to the `results.html` file and can be viewed in any web browser.

### Setup Assistant

The assistant will:
1. Check and install required dependencies
2. Help you configure execution frequency
3. Let you choose a specific speed test server or use automatic selection
4. Create the task in Windows Task Scheduler

### Manual Configuration

If you prefer to configure manually:
1. Open Windows "Task Scheduler"
2. Click "Create Basic Task"
3. Give it a name "WanMonitor"
4. Choose desired frequency (e.g., Daily)
5. In action, choose "Start a program"
6. In "Program/script" field, put Python path (e.g., C:\Python39\python.exe)
7. In "Arguments", put the full path to monitor.py
8. In "Start in", put the directory where the script is located

## Results

Results are stored in an HTML file with the following information:
- timestamp: Test date and time
- download: Download speed in Mbps
- upload: Upload speed in Mbps
- ping: Latency in milliseconds
- jitter: Latency variation in milliseconds
