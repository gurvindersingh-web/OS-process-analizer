#!/usr/bin/env python3
"""
OS Performance Analyzer - Main Entry Point

A workload generation toolkit for testing operating system performance.
Simulates CPU, memory, and disk stress with configurable load patterns,
real-time monitoring, and safe resource handling.
"""
import argparse
import sys
import time
import signal
from config import WorkloadConfig, get_preset_config
from workload_generator import WorkloadGenerator
from monitoring import SystemMonitor


class OSPerformanceAnalyzer:
    """Main orchestrator for the OS Performance Analyzer."""
    
    def __init__(self, config: WorkloadConfig):
        self.config = config
        self.workload_generator = WorkloadGenerator(config)
        self.monitor = SystemMonitor(interval=config.monitoring_interval)
        self.running = True
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        """Handle interrupt signals gracefully."""
        print("\n\nReceived interrupt signal. Shutting down gracefully...")
        self.running = False
        self.stop()
    
    def run(self):
        """Run the performance analyzer."""
        try:
            # Display initial system state
            print("\nInitial System State:")
            self.monitor.display_stats()
            
            # Start monitoring
            self.monitor.start_monitoring()
            
            # Start workload generation
            self.workload_generator.start_all()
            
            # Calculate total duration
            max_duration = max(
                self.config.cpu_duration if self.config.cpu_enabled else 0,
                self.config.memory_duration if self.config.memory_enabled else 0,
                self.config.disk_duration if self.config.disk_enabled else 0
            )
            
            # Monitor in real-time
            start_time = time.time()
            while self.running and (time.time() - start_time) < max_duration:
                time.sleep(self.config.monitoring_interval)
                stats = self.monitor.record_stats()
                
                if self.config.display_realtime and stats:
                    self.monitor.display_stats(stats)
            
            # Wait for workloads to complete
            print("\nWaiting for workloads to complete...")
            self.workload_generator.wait_all()
            
            # Stop monitoring
            self.monitor.stop_monitoring()
            
            # Display summary
            self.monitor.display_summary()
            
            print("\nPerformance analysis completed successfully!")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user.")
            self.stop()
        except Exception as e:
            print(f"\nError during execution: {e}")
            self.stop()
            sys.exit(1)
    
    def stop(self):
        """Stop all operations gracefully."""
        self.running = False
        self.workload_generator.stop_all()
        self.monitor.stop_monitoring()


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="OS Performance Analyzer - Workload Generation Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default moderate load
  python os_analyzer.py
  
  # Run with preset configuration
  python os_analyzer.py --preset heavy
  
  # Custom CPU-only test
  python os_analyzer.py --cpu-only --cpu-threads 4 --cpu-intensity 80 --duration 120
  
  # Custom memory test
  python os_analyzer.py --memory-only --memory-size 500 --duration 60
  
  # Load configuration from file
  python os_analyzer.py --config my_config.json
  
  # Save current configuration to file
  python os_analyzer.py --save-config my_config.json --preset heavy
        """
    )
    
    # Preset and configuration
    parser.add_argument('--preset', choices=['light', 'moderate', 'heavy', 'extreme'],
                        default='moderate', help='Preset load pattern')
    parser.add_argument('--config', type=str, help='Load configuration from JSON file')
    parser.add_argument('--save-config', type=str, help='Save configuration to JSON file and exit')
    
    # Workload selection
    parser.add_argument('--cpu-only', action='store_true', help='Run CPU workload only')
    parser.add_argument('--memory-only', action='store_true', help='Run memory workload only')
    parser.add_argument('--disk-only', action='store_true', help='Run disk workload only')
    
    # CPU configuration
    parser.add_argument('--cpu-threads', type=int, help='Number of CPU threads')
    parser.add_argument('--cpu-intensity', type=float, help='CPU intensity (0-100)')
    
    # Memory configuration
    parser.add_argument('--memory-size', type=int, help='Memory size in MB')
    parser.add_argument('--memory-pattern', choices=['sequential', 'random'], 
                        help='Memory access pattern')
    
    # Disk configuration
    parser.add_argument('--disk-files', type=int, help='Number of disk files')
    parser.add_argument('--disk-size', type=int, help='Size of each disk file in MB')
    parser.add_argument('--disk-pattern', choices=['sequential', 'random'],
                        help='Disk I/O pattern')
    parser.add_argument('--disk-dir', type=str, help='Disk work directory')
    
    # General configuration
    parser.add_argument('--duration', type=int, help='Test duration in seconds')
    parser.add_argument('--monitoring-interval', type=float, default=1.0,
                        help='Monitoring interval in seconds')
    parser.add_argument('--no-realtime', action='store_true',
                        help='Disable real-time display')
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Load configuration
    if args.config:
        print(f"Loading configuration from {args.config}")
        config = WorkloadConfig.from_json(args.config)
    else:
        config = get_preset_config(args.preset)
    
    # Apply command-line overrides
    if args.cpu_only:
        config.memory_enabled = False
        config.disk_enabled = False
    if args.memory_only:
        config.cpu_enabled = False
        config.disk_enabled = False
    if args.disk_only:
        config.cpu_enabled = False
        config.memory_enabled = False
    
    if args.cpu_threads is not None:
        config.cpu_threads = args.cpu_threads
    if args.cpu_intensity is not None:
        config.cpu_intensity = args.cpu_intensity
    
    if args.memory_size is not None:
        config.memory_size_mb = args.memory_size
    if args.memory_pattern is not None:
        config.memory_pattern = args.memory_pattern
    
    if args.disk_files is not None:
        config.disk_num_files = args.disk_files
    if args.disk_size is not None:
        config.disk_file_size_mb = args.disk_size
    if args.disk_pattern is not None:
        config.disk_pattern = args.disk_pattern
    if args.disk_dir is not None:
        config.disk_work_dir = args.disk_dir
    
    if args.duration is not None:
        config.cpu_duration = args.duration
        config.memory_duration = args.duration
        config.disk_duration = args.duration
    
    config.monitoring_interval = args.monitoring_interval
    config.display_realtime = not args.no_realtime
    
    # Save configuration if requested
    if args.save_config:
        print(f"Saving configuration to {args.save_config}")
        config.to_json(args.save_config)
        print("Configuration saved successfully!")
        return
    
    # Display configuration
    print("\n" + "="*60)
    print("OS PERFORMANCE ANALYZER")
    print("="*60)
    print(f"Preset: {args.preset}")
    print(f"\nWorkload Configuration:")
    print(f"  CPU:    {'Enabled' if config.cpu_enabled else 'Disabled'} "
          f"({config.cpu_threads} threads @ {config.cpu_intensity}% for {config.cpu_duration}s)")
    print(f"  Memory: {'Enabled' if config.memory_enabled else 'Disabled'} "
          f"({config.memory_size_mb} MB, {config.memory_pattern} pattern for {config.memory_duration}s)")
    print(f"  Disk:   {'Enabled' if config.disk_enabled else 'Disabled'} "
          f"({config.disk_num_files} files x {config.disk_file_size_mb} MB, {config.disk_pattern} pattern for {config.disk_duration}s)")
    print("="*60)
    
    # Run the analyzer
    analyzer = OSPerformanceAnalyzer(config)
    analyzer.run()


if __name__ == "__main__":
    main()
