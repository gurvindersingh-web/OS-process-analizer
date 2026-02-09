#!/usr/bin/env python3
"""
OS Performance Analyzer - Workload Generation Toolkit
Simulates CPU, memory, and disk stress with configurable load patterns,
real-time monitoring, and safe resource handling.
"""

import os
import sys
import time
import argparse
import threading
import multiprocessing
import psutil
import signal
from datetime import datetime
from typing import Optional, Dict, List


class ResourceMonitor:
    """Real-time system resource monitor."""
    
    def __init__(self, interval: float = 1.0):
        """
        Initialize the monitor.
        
        Args:
            interval: Monitoring interval in seconds
        """
        self.interval = interval
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.stats: List[Dict] = []
        
    def start(self):
        """Start monitoring in a separate thread."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop monitoring."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
            
    def _monitor_loop(self):
        """Monitor system resources continuously."""
        while self.running:
            try:
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_io_counters()
                
                stat = {
                    'timestamp': datetime.now().isoformat(),
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'memory_used_mb': memory.used / (1024 * 1024),
                    'memory_available_mb': memory.available / (1024 * 1024),
                    'disk_read_mb': disk.read_bytes / (1024 * 1024) if disk else 0,
                    'disk_write_mb': disk.write_bytes / (1024 * 1024) if disk else 0,
                }
                
                self.stats.append(stat)
                
                # Print real-time stats
                print(f"\r[{stat['timestamp']}] CPU: {cpu_percent:5.1f}% | "
                      f"Memory: {memory.percent:5.1f}% ({memory.used / (1024**3):.2f}GB) | "
                      f"Disk R/W: {stat['disk_read_mb']:.1f}/{stat['disk_write_mb']:.1f} MB",
                      end='', flush=True)
                
                time.sleep(self.interval)
            except Exception as e:
                print(f"\nMonitor error: {e}", file=sys.stderr)
                
    def get_summary(self) -> Dict:
        """Get summary statistics."""
        if not self.stats:
            return {}
            
        cpu_values = [s['cpu_percent'] for s in self.stats]
        mem_values = [s['memory_percent'] for s in self.stats]
        
        return {
            'duration_seconds': len(self.stats) * self.interval,
            'samples': len(self.stats),
            'cpu_avg': sum(cpu_values) / len(cpu_values),
            'cpu_max': max(cpu_values),
            'cpu_min': min(cpu_values),
            'memory_avg': sum(mem_values) / len(mem_values),
            'memory_max': max(mem_values),
            'memory_min': min(mem_values),
        }


class CPUStressor:
    """CPU workload simulator."""
    
    def __init__(self, num_threads: Optional[int] = None, intensity: float = 1.0):
        """
        Initialize CPU stressor.
        
        Args:
            num_threads: Number of threads to spawn (defaults to CPU count)
            intensity: Load intensity from 0.0 to 1.0
        """
        self.num_threads = num_threads or multiprocessing.cpu_count()
        self.intensity = max(0.0, min(1.0, intensity))
        self.running = False
        self.processes: List[multiprocessing.Process] = []
        
    def _cpu_work(self, duration: float):
        """CPU-intensive work function."""
        # Ignore signals in child processes
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        
        end_time = time.time() + duration
        while time.time() < end_time:
            # Work phase - intensive calculation
            work_duration = self.intensity * 0.1
            work_end = time.time() + work_duration
            while time.time() < work_end:
                # CPU-intensive operation
                _ = sum(i * i for i in range(1000))
            
            # Rest phase if intensity < 1.0
            if self.intensity < 1.0:
                time.sleep((1.0 - self.intensity) * 0.1)
                
    def start(self, duration: float = 10.0):
        """
        Start CPU stress test.
        
        Args:
            duration: Duration in seconds
        """
        print(f"\nStarting CPU stress test: {self.num_threads} threads, "
              f"intensity {self.intensity:.1%}, duration {duration}s")
        
        self.running = True
        for i in range(self.num_threads):
            p = multiprocessing.Process(target=self._cpu_work, args=(duration,))
            p.start()
            self.processes.append(p)
            
    def stop(self):
        """Stop CPU stress test."""
        self.running = False
        for p in self.processes:
            try:
                if p.is_alive():
                    p.terminate()
                    p.join(timeout=1)
                    if p.is_alive():
                        p.kill()
            except Exception:
                pass
        self.processes.clear()


class MemoryStressor:
    """Memory workload simulator with safe allocation."""
    
    def __init__(self, target_mb: int = 100, pattern: str = 'linear'):
        """
        Initialize memory stressor.
        
        Args:
            target_mb: Target memory allocation in MB
            pattern: Allocation pattern ('linear', 'burst', 'wave')
        """
        self.target_mb = target_mb
        self.pattern = pattern
        self.allocated: List[bytearray] = []
        self.running = False
        
    def _allocate_safe(self, size_mb: int) -> bool:
        """
        Safely allocate memory.
        
        Args:
            size_mb: Size to allocate in MB
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check available memory
            available = psutil.virtual_memory().available / (1024 * 1024)
            if available < size_mb * 2:  # Keep 2x buffer
                print(f"\nWarning: Insufficient memory available ({available:.0f}MB), skipping allocation")
                return False
                
            # Allocate and write to ensure it's actually allocated
            chunk = bytearray(size_mb * 1024 * 1024)
            for i in range(0, len(chunk), 4096):
                chunk[i] = i % 256
            self.allocated.append(chunk)
            return True
        except MemoryError:
            print("\nMemoryError: Cannot allocate more memory")
            return False
            
    def start(self, duration: float = 10.0):
        """
        Start memory stress test.
        
        Args:
            duration: Duration in seconds
        """
        print(f"\nStarting memory stress test: target {self.target_mb}MB, "
              f"pattern '{self.pattern}', duration {duration}s")
        
        self.running = True
        start_time = time.time()
        
        if self.pattern == 'linear':
            # Gradual linear allocation
            chunk_size = 10  # MB per step
            while self.running and time.time() - start_time < duration:
                if sum(len(a) for a in self.allocated) / (1024 * 1024) < self.target_mb:
                    self._allocate_safe(chunk_size)
                time.sleep(0.5)
                
        elif self.pattern == 'burst':
            # Quick burst allocation then hold
            chunk_size = 50  # MB per burst
            while self.running and sum(len(a) for a in self.allocated) / (1024 * 1024) < self.target_mb:
                if not self._allocate_safe(chunk_size):
                    break
                time.sleep(0.1)
            # Hold until duration
            while self.running and time.time() - start_time < duration:
                time.sleep(0.5)
                
        elif self.pattern == 'wave':
            # Allocate and deallocate in waves
            chunk_size = 20  # MB per wave
            while self.running and time.time() - start_time < duration:
                # Allocate phase
                for _ in range(3):
                    if not self._allocate_safe(chunk_size):
                        break
                    time.sleep(0.3)
                # Deallocate phase
                if len(self.allocated) > 2:
                    self.allocated = self.allocated[:-2]
                time.sleep(0.5)
                
    def stop(self):
        """Stop and cleanup memory."""
        self.running = False
        self.allocated.clear()
        print("\nMemory cleaned up")


class DiskStressor:
    """Disk I/O workload simulator."""
    
    def __init__(self, target_mb: int = 50, io_pattern: str = 'sequential'):
        """
        Initialize disk stressor.
        
        Args:
            target_mb: Target data size in MB
            io_pattern: I/O pattern ('sequential', 'random', 'mixed')
        """
        self.target_mb = target_mb
        self.io_pattern = io_pattern
        self.running = False
        self.test_dir = '/tmp/os_analyzer_test'
        
    def _setup(self):
        """Setup test directory."""
        os.makedirs(self.test_dir, exist_ok=True)
        
    def _cleanup(self):
        """Cleanup test files."""
        try:
            if os.path.exists(self.test_dir):
                for filename in os.listdir(self.test_dir):
                    filepath = os.path.join(self.test_dir, filename)
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                os.rmdir(self.test_dir)
        except Exception as e:
            # Silently ignore cleanup errors
            pass
            
    def start(self, duration: float = 10.0):
        """
        Start disk stress test.
        
        Args:
            duration: Duration in seconds
        """
        print(f"\nStarting disk I/O stress test: {self.target_mb}MB, "
              f"pattern '{self.io_pattern}', duration {duration}s")
        
        self._setup()
        self.running = True
        start_time = time.time()
        file_counter = 0
        
        try:
            if self.io_pattern == 'sequential':
                # Sequential writes and reads
                while self.running and time.time() - start_time < duration:
                    filepath = os.path.join(self.test_dir, f'test_{file_counter}.dat')
                    data = os.urandom(1024 * 1024)  # 1MB chunks
                    
                    # Write
                    with open(filepath, 'wb') as f:
                        for _ in range(min(10, self.target_mb // 10)):
                            f.write(data)
                    
                    # Read back
                    with open(filepath, 'rb') as f:
                        _ = f.read()
                    
                    file_counter += 1
                    time.sleep(0.1)
                    
            elif self.io_pattern == 'random':
                # Random access patterns
                filepath = os.path.join(self.test_dir, 'random_test.dat')
                data = os.urandom(self.target_mb * 1024 * 1024)
                
                with open(filepath, 'wb') as f:
                    f.write(data)
                
                # Random reads
                import random
                file_size = os.path.getsize(filepath)
                with open(filepath, 'rb') as f:
                    while self.running and time.time() - start_time < duration:
                        position = random.randint(0, max(0, file_size - 4096))
                        f.seek(position)
                        _ = f.read(4096)
                        time.sleep(0.01)
                        
            elif self.io_pattern == 'mixed':
                # Mixed sequential and random
                while self.running and time.time() - start_time < duration:
                    filepath = os.path.join(self.test_dir, f'mixed_{file_counter}.dat')
                    data = os.urandom(1024 * 1024)
                    
                    # Sequential write
                    with open(filepath, 'wb') as f:
                        for _ in range(5):
                            f.write(data)
                    
                    # Random read
                    with open(filepath, 'rb') as f:
                        f.seek(2 * 1024 * 1024)
                        _ = f.read(512 * 1024)
                    
                    file_counter += 1
                    time.sleep(0.2)
                    
        finally:
            self._cleanup()
            
    def stop(self):
        """Stop disk stress test."""
        self.running = False
        self._cleanup()


class PerformanceAnalyzer:
    """Main performance analyzer orchestrator."""
    
    def __init__(self):
        """Initialize the analyzer."""
        self.monitor = ResourceMonitor(interval=1.0)
        self.cpu_stressor: Optional[CPUStressor] = None
        self.mem_stressor: Optional[MemoryStressor] = None
        self.disk_stressor: Optional[DiskStressor] = None
        self.running = False
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print("\n\nReceived shutdown signal, cleaning up...")
        self.stop()
        sys.exit(0)
        
    def run(self, config: Dict):
        """
        Run performance analysis with given configuration.
        
        Args:
            config: Configuration dictionary
        """
        duration = config.get('duration', 10.0)
        
        print("=" * 70)
        print("OS Performance Analyzer - Workload Generation Toolkit")
        print("=" * 70)
        
        # Start monitoring
        self.monitor.start()
        time.sleep(0.5)
        
        self.running = True
        threads = []
        
        try:
            # Start CPU stress if configured
            if config.get('cpu_stress'):
                self.cpu_stressor = CPUStressor(
                    num_threads=config.get('cpu_threads'),
                    intensity=config.get('cpu_intensity', 1.0)
                )
                t = threading.Thread(target=self.cpu_stressor.start, args=(duration,))
                t.start()
                threads.append(t)
                time.sleep(0.5)
                
            # Start memory stress if configured
            if config.get('memory_stress'):
                self.mem_stressor = MemoryStressor(
                    target_mb=config.get('memory_mb', 100),
                    pattern=config.get('memory_pattern', 'linear')
                )
                t = threading.Thread(target=self.mem_stressor.start, args=(duration,))
                t.start()
                threads.append(t)
                time.sleep(0.5)
                
            # Start disk stress if configured
            if config.get('disk_stress'):
                self.disk_stressor = DiskStressor(
                    target_mb=config.get('disk_mb', 50),
                    io_pattern=config.get('disk_pattern', 'sequential')
                )
                t = threading.Thread(target=self.disk_stressor.start, args=(duration,))
                t.start()
                threads.append(t)
                
            # Wait for all stress tests to complete
            for t in threads:
                t.join()
                
        finally:
            self.stop()
            
        # Print summary
        self._print_summary()
        
    def stop(self):
        """Stop all stress tests and monitoring."""
        self.running = False
        
        if self.cpu_stressor:
            self.cpu_stressor.stop()
        if self.mem_stressor:
            self.mem_stressor.stop()
        if self.disk_stressor:
            self.disk_stressor.stop()
            
        self.monitor.stop()
        
    def _print_summary(self):
        """Print performance summary."""
        print("\n\n" + "=" * 70)
        print("Performance Analysis Summary")
        print("=" * 70)
        
        summary = self.monitor.get_summary()
        if summary:
            print(f"Duration: {summary['duration_seconds']:.1f} seconds")
            print(f"Samples: {summary['samples']}")
            print(f"\nCPU Usage:")
            print(f"  Average: {summary['cpu_avg']:.1f}%")
            print(f"  Maximum: {summary['cpu_max']:.1f}%")
            print(f"  Minimum: {summary['cpu_min']:.1f}%")
            print(f"\nMemory Usage:")
            print(f"  Average: {summary['memory_avg']:.1f}%")
            print(f"  Maximum: {summary['memory_max']:.1f}%")
            print(f"  Minimum: {summary['memory_min']:.1f}%")
            
            # Stability assessment
            cpu_variance = summary['cpu_max'] - summary['cpu_min']
            mem_variance = summary['memory_max'] - summary['memory_min']
            
            print(f"\nSystem Stability:")
            print(f"  CPU variance: {cpu_variance:.1f}%")
            print(f"  Memory variance: {mem_variance:.1f}%")
            
            if cpu_variance < 20 and mem_variance < 10:
                print("  Assessment: STABLE - Low resource variance")
            elif cpu_variance < 40 and mem_variance < 20:
                print("  Assessment: MODERATE - Medium resource variance")
            else:
                print("  Assessment: UNSTABLE - High resource variance detected")
                
            # Performance bottlenecks
            print(f"\nPotential Bottlenecks:")
            if summary['cpu_avg'] > 80:
                print("  ⚠ CPU - High average CPU utilization detected")
            if summary['memory_avg'] > 80:
                print("  ⚠ Memory - High average memory utilization detected")
            if summary['cpu_avg'] < 80 and summary['memory_avg'] < 80:
                print("  ✓ No significant bottlenecks detected")
        
        print("=" * 70)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='OS Performance Analyzer - Workload Generation Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # CPU stress test only
  %(prog)s --cpu --duration 30
  
  # Memory stress test with burst pattern
  %(prog)s --memory --memory-mb 200 --memory-pattern burst --duration 20
  
  # Disk I/O stress test
  %(prog)s --disk --disk-mb 100 --disk-pattern random --duration 15
  
  # Combined stress test
  %(prog)s --cpu --memory --disk --duration 60 --cpu-intensity 0.7
  
  # Full system stress
  %(prog)s --all --duration 120
        """
    )
    
    # General options
    parser.add_argument('--duration', type=float, default=10.0,
                       help='Test duration in seconds (default: 10)')
    parser.add_argument('--all', action='store_true',
                       help='Enable all stress tests')
    
    # CPU options
    parser.add_argument('--cpu', action='store_true',
                       help='Enable CPU stress test')
    parser.add_argument('--cpu-threads', type=int,
                       help='Number of CPU threads (default: CPU count)')
    parser.add_argument('--cpu-intensity', type=float, default=1.0,
                       help='CPU load intensity 0.0-1.0 (default: 1.0)')
    
    # Memory options
    parser.add_argument('--memory', action='store_true',
                       help='Enable memory stress test')
    parser.add_argument('--memory-mb', type=int, default=100,
                       help='Target memory allocation in MB (default: 100)')
    parser.add_argument('--memory-pattern', choices=['linear', 'burst', 'wave'],
                       default='linear',
                       help='Memory allocation pattern (default: linear)')
    
    # Disk options
    parser.add_argument('--disk', action='store_true',
                       help='Enable disk I/O stress test')
    parser.add_argument('--disk-mb', type=int, default=50,
                       help='Disk I/O data size in MB (default: 50)')
    parser.add_argument('--disk-pattern', choices=['sequential', 'random', 'mixed'],
                       default='sequential',
                       help='Disk I/O pattern (default: sequential)')
    
    args = parser.parse_args()
    
    # Build configuration
    config = {
        'duration': args.duration,
        'cpu_stress': args.cpu or args.all,
        'cpu_threads': args.cpu_threads,
        'cpu_intensity': args.cpu_intensity,
        'memory_stress': args.memory or args.all,
        'memory_mb': args.memory_mb,
        'memory_pattern': args.memory_pattern,
        'disk_stress': args.disk or args.all,
        'disk_mb': args.disk_mb,
        'disk_pattern': args.disk_pattern,
    }
    
    # Validate at least one test is enabled
    if not (config['cpu_stress'] or config['memory_stress'] or config['disk_stress']):
        parser.error('At least one stress test must be enabled (--cpu, --memory, --disk, or --all)')
    
    # Run analyzer
    analyzer = PerformanceAnalyzer()
    analyzer.run(config)


if __name__ == '__main__':
    main()
