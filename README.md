# OS Performance Analyzer

OS Performance Analyzer is a workload generation toolkit for testing operating system performance. It simulates CPU, memory, and disk stress with configurable load patterns, real-time monitoring, and safe resource handling, helping analyze system stability and detect performance bottlenecks.

## Features

- **CPU Stress Testing**: Simulate CPU-intensive workloads with configurable thread count and intensity levels
- **Memory Stress Testing**: Test memory allocation and deallocation with multiple patterns (linear, burst, wave)
- **Disk I/O Stress Testing**: Simulate disk operations with various patterns (sequential, random, mixed)
- **Real-time Monitoring**: Track CPU, memory, and disk usage in real-time during tests
- **Safe Resource Handling**: Automatic cleanup and safe allocation with availability checks
- **System Stability Analysis**: Assess system stability and detect performance bottlenecks
- **Flexible Configuration**: Command-line interface with extensive options

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gurvindersingh-web/OS-process-analizer.git
cd OS-process-analizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Examples

**CPU Stress Test:**
```bash
python os_analyzer.py --cpu --duration 30
```

**Memory Stress Test:**
```bash
python os_analyzer.py --memory --memory-mb 200 --memory-pattern burst --duration 20
```

**Disk I/O Stress Test:**
```bash
python os_analyzer.py --disk --disk-mb 100 --disk-pattern random --duration 15
```

**Combined Stress Test:**
```bash
python os_analyzer.py --cpu --memory --disk --duration 60 --cpu-intensity 0.7
```

**Full System Stress:**
```bash
python os_analyzer.py --all --duration 120
```

### Command-Line Options

#### General Options
- `--duration SECONDS`: Test duration in seconds (default: 10)
- `--all`: Enable all stress tests

#### CPU Options
- `--cpu`: Enable CPU stress test
- `--cpu-threads N`: Number of CPU threads (default: CPU count)
- `--cpu-intensity 0.0-1.0`: CPU load intensity (default: 1.0)

#### Memory Options
- `--memory`: Enable memory stress test
- `--memory-mb MB`: Target memory allocation in MB (default: 100)
- `--memory-pattern PATTERN`: Allocation pattern - `linear`, `burst`, or `wave` (default: linear)

#### Disk Options
- `--disk`: Enable disk I/O stress test
- `--disk-mb MB`: Disk I/O data size in MB (default: 50)
- `--disk-pattern PATTERN`: I/O pattern - `sequential`, `random`, or `mixed` (default: sequential)

### Load Patterns

#### Memory Patterns
- **Linear**: Gradual, steady memory allocation over time
- **Burst**: Quick burst of allocation followed by sustained hold
- **Wave**: Periodic allocation and deallocation cycles

#### Disk I/O Patterns
- **Sequential**: Sequential read and write operations
- **Random**: Random access patterns across the file
- **Mixed**: Combination of sequential writes and random reads

## Output

The tool provides:

1. **Real-time monitoring** during test execution showing:
   - CPU utilization percentage
   - Memory usage and percentage
   - Disk read/write operations

2. **Performance summary** after completion including:
   - Average, maximum, and minimum resource usage
   - System stability assessment
   - Potential bottleneck detection

### Example Output

```
======================================================================
OS Performance Analyzer - Workload Generation Toolkit
======================================================================

Starting CPU stress test: 8 threads, intensity 100.0%, duration 30.0s

Starting memory stress test: target 200MB, pattern 'linear', duration 30.0s

[2026-02-09T07:14:00] CPU: 95.2% | Memory: 45.3% (7.23GB) | Disk R/W: 0.0/0.0 MB

======================================================================
Performance Analysis Summary
======================================================================
Duration: 30.0 seconds
Samples: 30

CPU Usage:
  Average: 93.5%
  Maximum: 98.2%
  Minimum: 87.1%

Memory Usage:
  Average: 44.8%
  Maximum: 47.3%
  Minimum: 42.1%

System Stability:
  CPU variance: 11.1%
  Memory variance: 5.2%
  Assessment: STABLE - Low resource variance

Potential Bottlenecks:
  ⚠ CPU - High average CPU utilization detected
======================================================================
```

## Safety Features

- **Memory Safety**: Checks available memory before allocation to prevent system crashes
- **Graceful Cleanup**: Automatic cleanup of allocated resources on exit or interrupt (Ctrl+C)
- **Signal Handling**: Proper handling of SIGINT and SIGTERM for clean shutdown
- **Isolated Disk Testing**: Uses temporary directory (`/tmp/os_analyzer_test`) with automatic cleanup

## Requirements

- Python 3.6+
- psutil library (for system monitoring)
- Linux/Unix-based operating system (recommended)

## Use Cases

- **Performance Testing**: Benchmark system performance under various load conditions
- **Stability Testing**: Assess system stability during sustained stress
- **Bottleneck Detection**: Identify CPU, memory, or I/O bottlenecks
- **Capacity Planning**: Determine system limits and capacity thresholds
- **Regression Testing**: Verify performance consistency across system updates

## License

See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
