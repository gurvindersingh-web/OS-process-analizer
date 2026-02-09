#!/usr/bin/env python3
"""
Example usage scenarios for OS Performance Analyzer.

This file demonstrates various ways to use the OS Performance Analyzer toolkit.
"""

# Example 1: Using the tool from command line
# python os_analyzer.py --preset light --duration 30

# Example 2: Running CPU-only stress test
# python os_analyzer.py --cpu-only --cpu-threads 4 --cpu-intensity 80 --duration 60

# Example 3: Running memory-only stress test
# python os_analyzer.py --memory-only --memory-size 500 --duration 60

# Example 4: Running disk-only stress test
# python os_analyzer.py --disk-only --disk-files 10 --disk-size 20 --disk-pattern random

# Example 5: Using configuration files
# python os_analyzer.py --preset heavy --save-config my_test.json
# python os_analyzer.py --config my_test.json

# Example 6: Custom combined test
# python os_analyzer.py --cpu-threads 4 --cpu-intensity 75 --memory-size 200 --disk-files 5 --duration 90


# Programmatic usage example:
if __name__ == "__main__":
    from config import WorkloadConfig
    from workload_generator import WorkloadGenerator
    from monitoring import SystemMonitor
    import time
    
    print("Example: Programmatic usage of OS Performance Analyzer")
    print("="*60)
    
    # Create a custom configuration
    config = WorkloadConfig(
        cpu_enabled=True,
        cpu_threads=2,
        cpu_intensity=50.0,
        cpu_duration=10,
        memory_enabled=True,
        memory_size_mb=100,
        memory_duration=10,
        disk_enabled=False,  # Disable disk for this example
    )
    
    # Initialize components
    monitor = SystemMonitor(interval=1.0)
    workload = WorkloadGenerator(config)
    
    print("Starting custom workload...")
    
    # Start monitoring
    monitor.start_monitoring()
    
    # Start workload
    workload.start_all()
    
    # Monitor for duration
    for i in range(10):
        time.sleep(1)
        stats = monitor.record_stats()
        if i % 2 == 0:  # Display every 2 seconds
            monitor.display_stats(stats)
    
    # Wait for completion
    workload.wait_all()
    
    # Stop monitoring
    monitor.stop_monitoring()
    
    # Display summary
    monitor.display_summary()
    
    print("\nExample completed!")
