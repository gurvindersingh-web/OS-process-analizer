#!/usr/bin/env python3
"""
Example usage of OS Performance Analyzer as a Python module
This demonstrates how to use the analyzer programmatically
"""

from os_analyzer import PerformanceAnalyzer

def example_cpu_stress():
    """Example: CPU stress test only"""
    print("\n=== Example 1: CPU Stress Test ===")
    config = {
        'duration': 10.0,
        'cpu_stress': True,
        'cpu_threads': 2,
        'cpu_intensity': 0.7,
        'memory_stress': False,
        'disk_stress': False,
    }
    
    analyzer = PerformanceAnalyzer()
    analyzer.run(config)


def example_memory_stress():
    """Example: Memory stress with burst pattern"""
    print("\n=== Example 2: Memory Stress Test ===")
    config = {
        'duration': 10.0,
        'cpu_stress': False,
        'memory_stress': True,
        'memory_mb': 200,
        'memory_pattern': 'burst',
        'disk_stress': False,
    }
    
    analyzer = PerformanceAnalyzer()
    analyzer.run(config)


def example_disk_stress():
    """Example: Disk I/O with mixed pattern"""
    print("\n=== Example 3: Disk I/O Stress Test ===")
    config = {
        'duration': 10.0,
        'cpu_stress': False,
        'memory_stress': False,
        'disk_stress': True,
        'disk_mb': 50,
        'disk_pattern': 'mixed',
    }
    
    analyzer = PerformanceAnalyzer()
    analyzer.run(config)


def example_combined_stress():
    """Example: Combined stress test"""
    print("\n=== Example 4: Combined Stress Test ===")
    config = {
        'duration': 15.0,
        'cpu_stress': True,
        'cpu_threads': None,  # Use all CPUs
        'cpu_intensity': 0.6,
        'memory_stress': True,
        'memory_mb': 300,
        'memory_pattern': 'wave',
        'disk_stress': True,
        'disk_mb': 100,
        'disk_pattern': 'sequential',
    }
    
    analyzer = PerformanceAnalyzer()
    analyzer.run(config)


def example_custom_duration():
    """Example: Long-running stability test"""
    print("\n=== Example 5: Stability Test (Long Duration) ===")
    config = {
        'duration': 60.0,  # 1 minute
        'cpu_stress': True,
        'cpu_intensity': 0.5,
        'memory_stress': True,
        'memory_mb': 200,
        'memory_pattern': 'linear',
        'disk_stress': True,
        'disk_mb': 50,
        'disk_pattern': 'sequential',
    }
    
    analyzer = PerformanceAnalyzer()
    analyzer.run(config)


if __name__ == '__main__':
    import sys
    
    print("=" * 70)
    print("OS Performance Analyzer - Python Usage Examples")
    print("=" * 70)
    
    if len(sys.argv) > 1:
        example = sys.argv[1]
        
        if example == '1':
            example_cpu_stress()
        elif example == '2':
            example_memory_stress()
        elif example == '3':
            example_disk_stress()
        elif example == '4':
            example_combined_stress()
        elif example == '5':
            example_custom_duration()
        else:
            print(f"Unknown example: {example}")
            print("Usage: python examples.py [1|2|3|4|5]")
    else:
        print("\nAvailable examples:")
        print("  1 - CPU stress test")
        print("  2 - Memory stress test")
        print("  3 - Disk I/O stress test")
        print("  4 - Combined stress test")
        print("  5 - Long-running stability test")
        print("\nUsage: python examples.py [1|2|3|4|5]")
        print("   or: python examples.py")
        print("\nRunning example 1 (CPU stress test)...")
        example_cpu_stress()
