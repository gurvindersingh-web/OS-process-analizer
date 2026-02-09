"""Real-time system monitoring module."""
import psutil
import time
from typing import Dict
from datetime import datetime


class SystemMonitor:
    """Monitor system resources in real-time."""
    
    def __init__(self, interval: float = 1.0):
        """
        Initialize the system monitor.
        
        Args:
            interval: Monitoring interval in seconds
        """
        self.interval = interval
        self.monitoring = False
        self.start_time = None
        self.stats_history = []
        
    def get_current_stats(self) -> Dict:
        """Get current system statistics."""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_io_counters()
        
        stats = {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': cpu_percent,
            'cpu_count': psutil.cpu_count(),
            'memory_used_mb': memory.used / (1024 * 1024),
            'memory_available_mb': memory.available / (1024 * 1024),
            'memory_percent': memory.percent,
            'memory_total_mb': memory.total / (1024 * 1024),
        }
        
        if disk:
            stats.update({
                'disk_read_mb': disk.read_bytes / (1024 * 1024),
                'disk_write_mb': disk.write_bytes / (1024 * 1024),
                'disk_read_count': disk.read_count,
                'disk_write_count': disk.write_count,
            })
        
        return stats
    
    def start_monitoring(self):
        """Start monitoring session."""
        self.monitoring = True
        self.start_time = time.time()
        self.stats_history = []
        
    def stop_monitoring(self):
        """Stop monitoring session."""
        self.monitoring = False
        
    def record_stats(self):
        """Record current statistics to history."""
        if self.monitoring:
            stats = self.get_current_stats()
            self.stats_history.append(stats)
            return stats
        return None
    
    def display_stats(self, stats: Dict | None = None):
        """Display current statistics in a formatted way."""
        if stats is None:
            stats = self.get_current_stats()
        
        elapsed = time.time() - self.start_time if self.start_time else 0
        
        print("\n" + "="*60)
        print(f"OS Performance Monitor - Elapsed: {elapsed:.1f}s")
        print("="*60)
        print(f"CPU Usage:     {stats['cpu_percent']:6.2f}% ({stats['cpu_count']} cores)")
        print(f"Memory Usage:  {stats['memory_used_mb']:8.1f} MB / {stats['memory_total_mb']:8.1f} MB ({stats['memory_percent']:.1f}%)")
        print(f"Memory Avail:  {stats['memory_available_mb']:8.1f} MB")
        
        if 'disk_read_mb' in stats:
            print(f"Disk Read:     {stats['disk_read_mb']:8.1f} MB ({stats['disk_read_count']} ops)")
            print(f"Disk Write:    {stats['disk_write_mb']:8.1f} MB ({stats['disk_write_count']} ops)")
        
        print("="*60)
        
    def get_summary_stats(self) -> Dict:
        """Get summary statistics from the monitoring session."""
        if not self.stats_history:
            return {}
        
        cpu_values = [s['cpu_percent'] for s in self.stats_history]
        memory_values = [s['memory_percent'] for s in self.stats_history]
        
        summary = {
            'duration': time.time() - self.start_time if self.start_time else 0,
            'samples': len(self.stats_history),
            'cpu_avg': sum(cpu_values) / len(cpu_values),
            'cpu_max': max(cpu_values),
            'cpu_min': min(cpu_values),
            'memory_avg': sum(memory_values) / len(memory_values),
            'memory_max': max(memory_values),
            'memory_min': min(memory_values),
        }
        
        if 'disk_read_mb' in self.stats_history[-1]:
            initial_disk = self.stats_history[0]
            final_disk = self.stats_history[-1]
            summary['disk_read_total_mb'] = final_disk['disk_read_mb'] - initial_disk['disk_read_mb']
            summary['disk_write_total_mb'] = final_disk['disk_write_mb'] - initial_disk['disk_write_mb']
        
        return summary
    
    def display_summary(self):
        """Display summary statistics."""
        summary = self.get_summary_stats()
        
        if not summary:
            print("No monitoring data available.")
            return
        
        print("\n" + "="*60)
        print("PERFORMANCE SUMMARY")
        print("="*60)
        print(f"Test Duration:  {summary['duration']:.1f} seconds")
        print(f"Samples:        {summary['samples']}")
        print(f"\nCPU Statistics:")
        print(f"  Average:      {summary['cpu_avg']:.2f}%")
        print(f"  Maximum:      {summary['cpu_max']:.2f}%")
        print(f"  Minimum:      {summary['cpu_min']:.2f}%")
        print(f"\nMemory Statistics:")
        print(f"  Average:      {summary['memory_avg']:.2f}%")
        print(f"  Maximum:      {summary['memory_max']:.2f}%")
        print(f"  Minimum:      {summary['memory_min']:.2f}%")
        
        if 'disk_read_total_mb' in summary:
            print(f"\nDisk I/O Statistics:")
            print(f"  Total Read:   {summary['disk_read_total_mb']:.2f} MB")
            print(f"  Total Write:  {summary['disk_write_total_mb']:.2f} MB")
        
        print("="*60)
