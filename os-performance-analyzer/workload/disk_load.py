#!/usr/bin/env python3
"""
Disk I/O Load Generator
Generates configurable disk I/O load for testing system performance monitoring.
"""

import argparse
import os
import signal
import sys
import tempfile
import threading
import time
import random
from datetime import datetime


class DiskLoadGenerator:
    """Generate disk I/O load with configurable patterns."""
    
    def __init__(self, size_mb, operations, threads, duration):
        """
        Initialize disk I/O load generator.
        
        Args:
            size_mb: Size of files to create in MB
            operations: Type of operations ('read', 'write', 'mixed')
            threads: Number of concurrent I/O threads
            duration: Duration in seconds (0 for infinite)
        """
        self.size_mb = size_mb
        self.operations = operations
        self.thread_count = threads
        self.duration = duration
        self.running = True
        self.temp_dir = None
        self.temp_files = []
        self.threads = []
        self.io_stats = {
            'reads': 0,
            'writes': 0,
            'bytes_read': 0,
            'bytes_written': 0
        }
        self.stats_lock = threading.Lock()
        
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\n[Disk Load] Received signal {signum}, shutting down...")
        self.running = False
        
    def _create_temp_files(self):
        """Create temporary files for I/O operations."""
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp(prefix='disk_load_')
        print(f"[Disk Load] Created temp directory: {self.temp_dir}")
        
        # Create one file per thread
        chunk_size = 1024 * 1024  # 1MB chunks
        
        for i in range(self.thread_count):
            filename = os.path.join(self.temp_dir, f'load_file_{i}.dat')
            print(f"[Disk Load] Creating file {i+1}/{self.thread_count}: {os.path.basename(filename)} ({self.size_mb}MB)")
            
            # Write initial data
            with open(filename, 'wb') as f:
                remaining = self.size_mb * 1024 * 1024
                while remaining > 0 and self.running:
                    chunk = min(chunk_size, remaining)
                    # Write random data
                    data = random.randbytes(chunk)
                    f.write(data)
                    remaining -= chunk
                    
            if self.running:
                self.temp_files.append(filename)
                
        print(f"[Disk Load] Created {len(self.temp_files)} temporary files")
        
    def _io_worker(self, worker_id):
        """
        Perform I/O operations in a worker thread.
        
        Args:
            worker_id: Worker thread identifier
        """
        if worker_id >= len(self.temp_files):
            return
            
        filename = self.temp_files[worker_id]
        chunk_size = 64 * 1024  # 64KB chunks for I/O
        
        print(f"[Worker {worker_id}] Started I/O operations on {os.path.basename(filename)}")
        
        while self.running:
            try:
                # Determine operation type
                if self.operations == 'read':
                    do_read = True
                elif self.operations == 'write':
                    do_read = False
                else:  # mixed
                    do_read = random.choice([True, False])
                    
                if do_read:
                    # Read operation
                    with open(filename, 'rb') as f:
                        # Random seek
                        file_size = os.path.getsize(filename)
                        if file_size > chunk_size:
                            position = random.randint(0, file_size - chunk_size)
                            f.seek(position)
                        
                        # Read chunk
                        data = f.read(chunk_size)
                        
                        with self.stats_lock:
                            self.io_stats['reads'] += 1
                            self.io_stats['bytes_read'] += len(data)
                else:
                    # Write operation
                    with open(filename, 'r+b') as f:
                        # Random seek
                        file_size = os.path.getsize(filename)
                        if file_size > chunk_size:
                            position = random.randint(0, file_size - chunk_size)
                            f.seek(position)
                        
                        # Write random data
                        data = random.randbytes(chunk_size)
                        f.write(data)
                        f.flush()
                        os.fsync(f.fileno())  # Force write to disk
                        
                        with self.stats_lock:
                            self.io_stats['writes'] += 1
                            self.io_stats['bytes_written'] += len(data)
                            
            except Exception as e:
                if self.running:
                    print(f"[Worker {worker_id}] Error: {e}")
                break
                
        print(f"[Worker {worker_id}] Stopped")
        
    def _stats_reporter(self):
        """Report I/O statistics periodically."""
        last_report = time.time()
        
        while self.running:
            time.sleep(5)  # Report every 5 seconds
            
            if not self.running:
                break
                
            with self.stats_lock:
                elapsed = time.time() - last_report
                
                read_mb = self.io_stats['bytes_read'] / (1024 * 1024)
                write_mb = self.io_stats['bytes_written'] / (1024 * 1024)
                
                read_rate = read_mb / elapsed if elapsed > 0 else 0
                write_rate = write_mb / elapsed if elapsed > 0 else 0
                
                print(f"[Stats] Reads: {self.io_stats['reads']} ({read_rate:.2f} MB/s), "
                      f"Writes: {self.io_stats['writes']} ({write_rate:.2f} MB/s)")
                
                # Reset stats for next period
                self.io_stats = {
                    'reads': 0,
                    'writes': 0,
                    'bytes_read': 0,
                    'bytes_written': 0
                }
                last_report = time.time()
                
    def _cleanup(self):
        """Clean up temporary files and directory."""
        print("[Disk Load] Cleaning up temporary files...")
        
        for filename in self.temp_files:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
                    print(f"[Disk Load] Removed {os.path.basename(filename)}")
            except Exception as e:
                print(f"[Disk Load] Error removing {filename}: {e}")
                
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                os.rmdir(self.temp_dir)
                print(f"[Disk Load] Removed temp directory: {self.temp_dir}")
            except Exception as e:
                print(f"[Disk Load] Error removing directory: {e}")
                
    def run(self):
        """Start disk I/O load generation."""
        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        print(f"[Disk Load] Starting disk I/O load generator")
        print(f"[Disk Load] File size: {self.size_mb}MB per file")
        print(f"[Disk Load] Operations: {self.operations}")
        print(f"[Disk Load] Threads: {self.thread_count}")
        print(f"[Disk Load] Duration: {self.duration}s" if self.duration > 0 else "[Disk Load] Duration: Infinite (Ctrl+C to stop)")
        print(f"[Disk Load] Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        try:
            # Create temporary files
            self._create_temp_files()
            
            if not self.running or len(self.temp_files) == 0:
                return
                
            # Start stats reporter thread
            stats_thread = threading.Thread(target=self._stats_reporter, daemon=True)
            stats_thread.start()
            
            # Start worker threads
            for i in range(self.thread_count):
                t = threading.Thread(target=self._io_worker, args=(i,))
                t.start()
                self.threads.append(t)
                
            # Wait for duration or interrupt
            if self.duration > 0:
                time.sleep(self.duration)
                self.running = False
            else:
                # Wait for interrupt
                while self.running:
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print("\n[Disk Load] Interrupted by user")
            self.running = False
            
        finally:
            # Wait for threads to finish
            print("[Disk Load] Stopping worker threads...")
            for i, t in enumerate(self.threads):
                t.join(timeout=2)
                if t.is_alive():
                    print(f"[Worker {i}] Still running, will force stop")
                    
            # Clean up files
            self._cleanup()
            
            print(f"[Disk Load] Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("[Disk Load] All workers terminated and files cleaned up")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate disk I/O load for system performance testing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Mixed read/write on 4 threads with 50MB files for 60 seconds
  %(prog)s --size 50 --operations mixed --threads 4 --duration 60
  
  # Write-only test with 2 threads indefinitely
  %(prog)s --size 100 --operations write --threads 2
  
  # Read-only test with 8 threads for 30 seconds
  %(prog)s --size 25 --operations read --threads 8 --duration 30
        """
    )
    
    parser.add_argument(
        '--size',
        type=int,
        default=50,
        help='Size of each file in MB (default: 50)'
    )
    
    parser.add_argument(
        '--operations',
        type=str,
        choices=['read', 'write', 'mixed'],
        default='mixed',
        help='Type of I/O operations (default: mixed)'
    )
    
    parser.add_argument(
        '--threads',
        type=int,
        default=4,
        help='Number of concurrent I/O threads (default: 4)'
    )
    
    parser.add_argument(
        '--duration',
        type=int,
        default=0,
        help='Duration in seconds (0 = infinite, default: 0)'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if args.size <= 0:
        print("Error: Size must be > 0")
        sys.exit(1)
        
    if args.threads <= 0:
        print("Error: Threads must be > 0")
        sys.exit(1)
        
    if args.duration < 0:
        print("Error: Duration must be >= 0")
        sys.exit(1)
        
    # Run the load generator
    generator = DiskLoadGenerator(args.size, args.operations, args.threads, args.duration)
    generator.run()


if __name__ == '__main__':
    main()
