#!/usr/bin/env python3
"""
CPU Load Generator
Generates configurable CPU load for testing system performance monitoring.
"""

import argparse
import multiprocessing
import signal
import sys
import time
from datetime import datetime


class CPULoadGenerator:
    """Generate CPU load using worker processes."""
    
    def __init__(self, cores, duration, intensity):
        """
        Initialize CPU load generator.
        
        Args:
            cores: Number of CPU cores to stress
            duration: Duration in seconds (0 for infinite)
            intensity: Load intensity (0-100%)
        """
        self.cores = cores
        self.duration = duration
        self.intensity = max(0, min(100, intensity))  # Clamp to 0-100
        self.processes = []
        self.running = True
        
    def _cpu_intensive_task(self, worker_id):
        """
        Perform CPU-intensive calculations.
        
        Args:
            worker_id: Worker process identifier
        """
        print(f"[Worker {worker_id}] Started on PID {multiprocessing.current_process().pid}")
        
        # Calculate work/sleep ratio based on intensity
        work_time = self.intensity / 100.0
        sleep_time = 1.0 - work_time
        
        while self.running:
            start = time.time()
            
            # Perform CPU-intensive work
            if work_time > 0:
                end_work = start + work_time
                while time.time() < end_work and self.running:
                    # Math operations to keep CPU busy
                    _ = sum(i * i for i in range(1000))
            
            # Sleep to achieve desired intensity
            if sleep_time > 0 and self.running:
                time.sleep(sleep_time)
                
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\n[CPU Load] Received signal {signum}, shutting down...")
        self.running = False
        
    def run(self):
        """Start CPU load generation."""
        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        print(f"[CPU Load] Starting CPU load generator")
        print(f"[CPU Load] Cores: {self.cores}")
        print(f"[CPU Load] Intensity: {self.intensity}%")
        print(f"[CPU Load] Duration: {self.duration}s" if self.duration > 0 else "[CPU Load] Duration: Infinite (Ctrl+C to stop)")
        print(f"[CPU Load] Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        # Start worker processes
        for i in range(self.cores):
            p = multiprocessing.Process(target=self._cpu_intensive_task, args=(i,))
            p.start()
            self.processes.append(p)
            
        try:
            # Wait for specified duration or until interrupted
            if self.duration > 0:
                time.sleep(self.duration)
                self.running = False
            else:
                # Infinite run - wait for signal
                while self.running:
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print("\n[CPU Load] Interrupted by user")
            self.running = False
            
        finally:
            # Clean up processes
            print("[CPU Load] Stopping worker processes...")
            for i, p in enumerate(self.processes):
                p.terminate()
                p.join(timeout=2)
                if p.is_alive():
                    print(f"[Worker {i}] Force killing...")
                    p.kill()
                    p.join()
                else:
                    print(f"[Worker {i}] Stopped")
                    
            print(f"[CPU Load] Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("[CPU Load] All workers terminated successfully")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate CPU load for system performance testing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Stress 2 cores at 50% intensity for 30 seconds
  %(prog)s --cores 2 --duration 30 --intensity 50
  
  # Stress all cores at 100% intensity indefinitely
  %(prog)s --cores 0 --intensity 100
  
  # Light load on 4 cores for 1 minute
  %(prog)s --cores 4 --duration 60 --intensity 25
        """
    )
    
    parser.add_argument(
        '--cores',
        type=int,
        default=0,
        help='Number of CPU cores to stress (0 = all available cores, default: 0)'
    )
    
    parser.add_argument(
        '--duration',
        type=int,
        default=0,
        help='Duration in seconds (0 = infinite, default: 0)'
    )
    
    parser.add_argument(
        '--intensity',
        type=int,
        default=100,
        help='Load intensity percentage 0-100 (default: 100)'
    )
    
    args = parser.parse_args()
    
    # Determine number of cores
    available_cores = multiprocessing.cpu_count()
    cores = args.cores if args.cores > 0 else available_cores
    
    if cores > available_cores:
        print(f"Warning: Requested {cores} cores but only {available_cores} available")
        print(f"Using {available_cores} cores instead")
        cores = available_cores
        
    # Validate inputs
    if args.duration < 0:
        print("Error: Duration must be >= 0")
        sys.exit(1)
        
    if not 0 <= args.intensity <= 100:
        print("Error: Intensity must be between 0 and 100")
        sys.exit(1)
        
    # Run the load generator
    generator = CPULoadGenerator(cores, args.duration, args.intensity)
    generator.run()


if __name__ == '__main__':
    main()
