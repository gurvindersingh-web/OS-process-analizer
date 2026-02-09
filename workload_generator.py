"""Workload generation module for CPU, Memory, and Disk stress testing."""
import os
import time
import threading
import random
import math
from typing import List
from config import WorkloadConfig


class CPUWorkload:
    """Generate CPU-intensive workload."""
    
    def __init__(self, config: WorkloadConfig):
        self.config = config
        self.running = False
        self.threads = []
        
    def cpu_stress_worker(self, intensity: float, duration: int):
        """
        Worker thread that stresses CPU.
        
        Args:
            intensity: CPU load intensity (0-100%)
            duration: Duration in seconds
        """
        end_time = time.time() + duration
        work_time = intensity / 100.0
        sleep_time = 1.0 - work_time
        
        while time.time() < end_time and self.running:
            # Perform CPU-intensive calculations
            start = time.time()
            while time.time() - start < work_time:
                # Complex mathematical operations
                _ = math.sqrt(random.random()) * math.sin(random.random())
                _ = sum([i ** 2 for i in range(100)])
            
            # Sleep to control intensity
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    def start(self):
        """Start CPU workload generation."""
        if not self.config.cpu_enabled:
            print("CPU workload disabled.")
            return
        
        self.running = True
        print(f"Starting CPU workload: {self.config.cpu_threads} threads, {self.config.cpu_intensity}% intensity")
        
        for i in range(self.config.cpu_threads):
            thread = threading.Thread(
                target=self.cpu_stress_worker,
                args=(self.config.cpu_intensity, self.config.cpu_duration),
                daemon=True
            )
            thread.start()
            self.threads.append(thread)
    
    def stop(self):
        """Stop CPU workload generation."""
        self.running = False
        
    def wait(self):
        """Wait for all CPU threads to complete."""
        for thread in self.threads:
            thread.join()


class MemoryWorkload:
    """Generate memory-intensive workload."""
    
    def __init__(self, config: WorkloadConfig):
        self.config = config
        self.running = False
        self.allocated_data = []
        self.thread = None
        
    def memory_stress_worker(self):
        """Worker thread that stresses memory."""
        size_bytes = self.config.memory_size_mb * 1024 * 1024
        chunk_size = 1024 * 1024  # 1MB chunks
        num_chunks = size_bytes // chunk_size
        
        print(f"Allocating {self.config.memory_size_mb} MB of memory...")
        
        try:
            # Allocate memory
            for i in range(num_chunks):
                if not self.running:
                    break
                
                if self.config.memory_pattern == "sequential":
                    # Sequential pattern
                    data = bytearray(b'\x00' * chunk_size)
                    for j in range(0, chunk_size, 4096):
                        data[j] = (i + j) % 256
                else:
                    # Random pattern
                    data = bytearray(random.getrandbits(8) for _ in range(chunk_size))
                
                self.allocated_data.append(data)
            
            print(f"Memory allocated successfully: {len(self.allocated_data)} MB")
            
            # Hold memory for the duration
            end_time = time.time() + self.config.memory_duration
            while time.time() < end_time and self.running:
                # Periodically access memory to prevent optimization
                if self.allocated_data:
                    chunk = random.choice(self.allocated_data)
                    _ = chunk[random.randint(0, len(chunk) - 1)]
                time.sleep(1)
        
        except MemoryError:
            print("Warning: Unable to allocate requested memory. Reducing allocation.")
        
        finally:
            # Clean up
            self.allocated_data.clear()
            print("Memory released.")
    
    def start(self):
        """Start memory workload generation."""
        if not self.config.memory_enabled:
            print("Memory workload disabled.")
            return
        
        self.running = True
        print(f"Starting memory workload: {self.config.memory_size_mb} MB, {self.config.memory_pattern} pattern")
        
        self.thread = threading.Thread(target=self.memory_stress_worker, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop memory workload generation."""
        self.running = False
        self.allocated_data.clear()
        
    def wait(self):
        """Wait for memory thread to complete."""
        if self.thread:
            self.thread.join()


class DiskWorkload:
    """Generate disk I/O intensive workload."""
    
    def __init__(self, config: WorkloadConfig):
        self.config = config
        self.running = False
        self.files_created = []
        self.thread = None
        
    def ensure_work_directory(self):
        """Ensure work directory exists."""
        os.makedirs(self.config.disk_work_dir, exist_ok=True)
        
    def disk_stress_worker(self):
        """Worker thread that stresses disk I/O."""
        try:
            self.ensure_work_directory()
            
            file_size_bytes = self.config.disk_file_size_mb * 1024 * 1024
            chunk_size = 1024 * 1024  # 1MB chunks
            
            print(f"Starting disk I/O: {self.config.disk_num_files} files x {self.config.disk_file_size_mb} MB")
            
            # Write phase
            for i in range(self.config.disk_num_files):
                if not self.running:
                    break
                
                filename = os.path.join(self.config.disk_work_dir, f"test_file_{i}.dat")
                self.files_created.append(filename)
                
                with open(filename, 'wb') as f:
                    bytes_written = 0
                    while bytes_written < file_size_bytes and self.running:
                        if self.config.disk_pattern == "sequential":
                            data = bytes([i % 256] * chunk_size)
                        else:
                            data = bytes(random.getrandbits(8) for _ in range(chunk_size))
                        
                        f.write(data)
                        bytes_written += chunk_size
                
                print(f"  Created: {filename}")
            
            # Read phase
            print("Reading files...")
            for filename in self.files_created:
                if not self.running:
                    break
                
                with open(filename, 'rb') as f:
                    while self.running:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                
                print(f"  Read: {filename}")
            
            # Hold for duration
            elapsed = 0
            while elapsed < self.config.disk_duration and self.running:
                time.sleep(1)
                elapsed += 1
        
        except Exception as e:
            print(f"Disk workload error: {e}")
        
        finally:
            # Cleanup
            self.cleanup()
    
    def cleanup(self):
        """Clean up created files and directories."""
        print("Cleaning up disk workload files...")
        for filename in self.files_created:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
            except Exception as e:
                print(f"Warning: Could not remove {filename}: {e}")
        
        self.files_created.clear()
        
        # Remove work directory if empty
        try:
            if os.path.exists(self.config.disk_work_dir):
                if not os.listdir(self.config.disk_work_dir):
                    os.rmdir(self.config.disk_work_dir)
        except Exception as e:
            print(f"Warning: Could not remove work directory: {e}")
    
    def start(self):
        """Start disk workload generation."""
        if not self.config.disk_enabled:
            print("Disk workload disabled.")
            return
        
        self.running = True
        print(f"Starting disk workload: {self.config.disk_num_files} files, {self.config.disk_pattern} pattern")
        
        self.thread = threading.Thread(target=self.disk_stress_worker, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop disk workload generation."""
        self.running = False
        
    def wait(self):
        """Wait for disk thread to complete."""
        if self.thread:
            self.thread.join()


class WorkloadGenerator:
    """Main workload generator that coordinates all stress tests."""
    
    def __init__(self, config: WorkloadConfig):
        self.config = config
        self.cpu_workload = CPUWorkload(config)
        self.memory_workload = MemoryWorkload(config)
        self.disk_workload = DiskWorkload(config)
        
    def start_all(self):
        """Start all enabled workloads."""
        print("\n" + "="*60)
        print("Starting OS Performance Analyzer Workload")
        print("="*60)
        
        if self.config.cpu_enabled:
            self.cpu_workload.start()
        
        if self.config.memory_enabled:
            self.memory_workload.start()
        
        if self.config.disk_enabled:
            self.disk_workload.start()
        
        print("="*60)
        
    def stop_all(self):
        """Stop all workloads."""
        print("\nStopping all workloads...")
        self.cpu_workload.stop()
        self.memory_workload.stop()
        self.disk_workload.stop()
        
    def wait_all(self):
        """Wait for all workloads to complete."""
        self.cpu_workload.wait()
        self.memory_workload.wait()
        self.disk_workload.wait()
