# OS Performance Analyzer

OS Performance Analyzer is a comprehensive workload generation toolkit for testing operating system performance. It simulates CPU, memory, and disk stress with configurable load patterns, real-time monitoring, and safe resource handling, helping analyze system stability and detect performance bottlenecks.

## Features

- **CPU Stress Testing**: Multi-threaded CPU-intensive workloads with configurable intensity (0-100%)
- **Memory Stress Testing**: Configurable memory allocation with sequential or random access patterns
- **Disk I/O Stress Testing**: Sequential and random disk I/O operations with multiple files
- **Real-time Monitoring**: Live system resource monitoring (CPU, memory, disk I/O)
- **Preset Load Patterns**: Pre-configured light, moderate, heavy, and extreme load patterns
- **Configurable Duration**: Set custom duration for each workload component
- **Safe Resource Handling**: Automatic cleanup and graceful shutdown on interruption
- **Summary Statistics**: Detailed performance summary after test completion
- **JSON Configuration**: Save and load test configurations from files

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### Run with Default Configuration (Moderate Load)

```bash
python os_analyzer.py
```

### Run with Preset Load Patterns

```bash
# Light load
python os_analyzer.py --preset light

# Moderate load (default)
python os_analyzer.py --preset moderate

# Heavy load
python os_analyzer.py --preset heavy

# Extreme load
python os_analyzer.py --preset extreme
```

## Usage Examples

### CPU-Only Test

```bash
# Run CPU stress test with 4 threads at 80% intensity for 120 seconds
python os_analyzer.py --cpu-only --cpu-threads 4 --cpu-intensity 80 --duration 120
```

### Memory-Only Test

```bash
# Allocate 500 MB of memory for 60 seconds
python os_analyzer.py --memory-only --memory-size 500 --duration 60
```

### Disk-Only Test

```bash
# Create 10 files of 20 MB each with random I/O pattern
python os_analyzer.py --disk-only --disk-files 10 --disk-size 20 --disk-pattern random
```

### Custom Combined Test

```bash
# Custom test with all workloads
python os_analyzer.py \
  --cpu-threads 4 \
  --cpu-intensity 75 \
  --memory-size 200 \
  --disk-files 5 \
  --disk-size 10 \
  --duration 90
```

### Configuration File Management

```bash
# Save a configuration to file
python os_analyzer.py --preset heavy --save-config my_test.json

# Load and run from configuration file
python os_analyzer.py --config my_test.json
```

## Command-Line Options

### Preset and Configuration
- `--preset {light,moderate,heavy,extreme}`: Select a preset load pattern (default: moderate)
- `--config FILE`: Load configuration from JSON file
- `--save-config FILE`: Save configuration to JSON file and exit

### Workload Selection
- `--cpu-only`: Run CPU workload only
- `--memory-only`: Run memory workload only
- `--disk-only`: Run disk workload only

### CPU Configuration
- `--cpu-threads N`: Number of CPU threads to use
- `--cpu-intensity N`: CPU intensity percentage (0-100)

### Memory Configuration
- `--memory-size N`: Memory size to allocate in MB
- `--memory-pattern {sequential,random}`: Memory access pattern

### Disk Configuration
- `--disk-files N`: Number of disk files to create
- `--disk-size N`: Size of each disk file in MB
- `--disk-pattern {sequential,random}`: Disk I/O pattern
- `--disk-dir PATH`: Directory for disk operations (default: /tmp/os_analyzer)

### General Configuration
- `--duration N`: Test duration in seconds (applies to all workloads)
- `--monitoring-interval N`: Monitoring interval in seconds (default: 1.0)
- `--no-realtime`: Disable real-time statistics display

## Preset Load Patterns

| Preset   | CPU Threads | CPU Intensity | Memory (MB) | Disk Files | File Size (MB) |
|----------|-------------|---------------|-------------|------------|----------------|
| Light    | 1           | 25%           | 50          | 3          | 5              |
| Moderate | 2           | 50%           | 100         | 5          | 10             |
| Heavy    | 4           | 75%           | 200         | 10         | 20             |
| Extreme  | 8           | 90%           | 500         | 20         | 50             |

## Output and Monitoring

The tool provides real-time monitoring during execution and a comprehensive summary at the end:

### Real-time Display

```
============================================================
OS Performance Monitor - Elapsed: 15.3s
============================================================
CPU Usage:      45.20% (4 cores)
Memory Usage:   2048.5 MB /  8192.0 MB (25.0%)
Memory Avail:   6143.5 MB
Disk Read:       150.2 MB (1250 ops)
Disk Write:      200.5 MB (1670 ops)
============================================================
```

### Summary Statistics

```
============================================================
PERFORMANCE SUMMARY
============================================================
Test Duration:  60.0 seconds
Samples:        60

CPU Statistics:
  Average:      48.32%
  Maximum:      75.50%
  Minimum:      15.20%

Memory Statistics:
  Average:      28.45%
  Maximum:      32.10%
  Minimum:      25.00%

Disk I/O Statistics:
  Total Read:   450.25 MB
  Total Write:  550.75 MB
============================================================
```

## Safety Features

- **Graceful Shutdown**: Responds to CTRL+C (SIGINT) and SIGTERM signals
- **Automatic Cleanup**: Removes all temporary disk files after test completion
- **Memory Error Handling**: Safely handles memory allocation failures
- **Resource Limits**: Configurable limits prevent system overload

## Use Cases

1. **Performance Testing**: Benchmark system performance under various load conditions
2. **Stability Testing**: Test system stability under sustained stress
3. **Bottleneck Detection**: Identify CPU, memory, or I/O bottlenecks
4. **Configuration Tuning**: Test impact of system configuration changes
5. **Capacity Planning**: Determine system capacity limits
6. **Regression Testing**: Verify performance after system updates

## Architecture

The toolkit consists of four main modules:

- **os_analyzer.py**: Main entry point and CLI interface
- **workload_generator.py**: CPU, memory, and disk workload generators
- **monitoring.py**: Real-time system resource monitoring
- **config.py**: Configuration management and preset patterns

## Requirements

- **psutil**: Cross-platform library for system and process monitoring

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Safety Notes

⚠️ **Warning**: This tool generates significant system load. Use with caution:

- Start with light or moderate presets to understand system behavior
- Monitor system temperature and resource usage
- Avoid running on production systems under active load
- Ensure adequate system cooling
- Stop immediately if system becomes unstable

## Troubleshooting

### Memory Allocation Errors

If you encounter memory allocation errors, reduce the `--memory-size` parameter or use a lower preset.

### Disk Space Issues

Ensure sufficient disk space is available. The tool requires approximately `disk_files * disk_size` MB of free space.

### Permission Errors

If disk operations fail due to permissions, specify a writable directory with `--disk-dir`.

## Support

For issues, questions, or contributions, please visit the project repository.
