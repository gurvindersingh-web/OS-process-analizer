#!/usr/bin/env python3
"""
Memory Load Generator
Generates configurable memory load for testing system performance monitoring.
"""

import argparse
import signal
import sys
import time
import random
from datetime import datetime


class MemoryLoadGenerator:
    """Generate memory load with configurable patterns."""
    
    def __init__(self, size_mb, duration, pattern):
        """
        Initialize memory load generator.
        
        Args:
            size_mb: Amount of memory to allocate in MB
            duration: Duration in seconds (0 for infinite)
            pattern: Access pattern ('sequential' or 'random')
        """
        self.size_mb = size_mb
        self.duration = duration
        self.pattern = pattern
        self.running = True
        self.memory_blocks = []
        
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\n[Memory Load] Received signal {signum}, shutting down...")
        self.running = False
        
    def _get_available_memory_mb(self):
        """Get available system memory in MB."""
        try:
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if 'MemAvailable' in line:
                        # Extract KB and convert to MB
                        available_kb = int(line.split()[1])
                        return available_kb // 1024
        except Exception:
            # Fallback if we can't read meminfo
            return None
            
    def _allocate_memory(self):
        """Allocate the specified amount of memory."""
        # Check available memory for safety
        available_mb = self._get_available_memory_mb()
        if available_mb and self.size_mb > available_mb * 0.8:
            print(f"[Memory Load] WARNING: Requested {self.size_mb}MB but only {available_mb}MB available")
            print(f"[Memory Load] Limiting allocation to {int(available_mb * 0.7)}MB for safety")
            self.size_mb = int(available_mb * 0.7)
            
        print(f"[Memory Load] Allocating {self.size_mb}MB of memory...")
        
        # Allocate memory in chunks (each chunk is ~1MB)
        chunk_size = 1024 * 1024 // 8  # 1MB in 8-byte integers
        
        for i in range(self.size_mb):
            if not self.running:
                break
                
            # Allocate a list of integers (8 bytes each)
            chunk = [random.randint(0, 1000000) for _ in range(chunk_size)]
            self.memory_blocks.append(chunk)
            
            # Progress indicator
            if (i + 1) % 100 == 0:
                print(f"[Memory Load] Allocated {i + 1}MB / {self.size_mb}MB")
                
        actual_allocated = len(self.memory_blocks)
        print(f"[Memory Load] Successfully allocated {actual_allocated}MB")
        
    def _access_memory_sequential(self):
        """Access memory in sequential pattern."""
        print("[Memory Load] Accessing memory (sequential pattern)...")
        
        for block_idx, block in enumerate(self.memory_blocks):
            if not self.running:
                break
                
            # Read and modify values sequentially
            for i in range(0, len(block), 1000):  # Sample every 1000th element
                if not self.running:
                    break
                _ = block[i]
                block[i] = (block[i] + 1) % 1000000
                
            if (block_idx + 1) % 100 == 0:
                print(f"[Memory Load] Processed {block_idx + 1}MB / {len(self.memory_blocks)}MB")
                
    def _access_memory_random(self):
        """Access memory in random pattern."""
        print("[Memory Load] Accessing memory (random pattern)...")
        
        total_blocks = len(self.memory_blocks)
        if total_blocks == 0:
            return
            
        iterations = 0
        while self.running:
            # Randomly select a block and index
            block_idx = random.randint(0, total_blocks - 1)
            block = self.memory_blocks[block_idx]
            
            if len(block) > 0:
                idx = random.randint(0, len(block) - 1)
                _ = block[idx]
                block[idx] = (block[idx] + 1) % 1000000
                
            iterations += 1
            if iterations % 10000 == 0:
                print(f"[Memory Load] Random accesses: {iterations}")
                
            # Small sleep to prevent 100% CPU usage
            if iterations % 1000 == 0:
                time.sleep(0.01)
                
    def run(self):
        """Start memory load generation."""
        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        print(f"[Memory Load] Starting memory load generator")
        print(f"[Memory Load] Size: {self.size_mb}MB")
        print(f"[Memory Load] Pattern: {self.pattern}")
        print(f"[Memory Load] Duration: {self.duration}s" if self.duration > 0 else "[Memory Load] Duration: Infinite (Ctrl+C to stop)")
        print(f"[Memory Load] Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        try:
            # Allocate memory
            self._allocate_memory()
            
            if not self.running:
                return
                
            # Access memory based on pattern
            start_time = time.time()
            
            while self.running:
                if self.pattern == 'sequential':
                    self._access_memory_sequential()
                else:  # random
                    self._access_memory_random()
                    
                # Check duration
                if self.duration > 0:
                    elapsed = time.time() - start_time
                    if elapsed >= self.duration:
                        self.running = False
                        
        except KeyboardInterrupt:
            print("\n[Memory Load] Interrupted by user")
            self.running = False
            
        except MemoryError:
            print("\n[Memory Load] ERROR: Out of memory!")
            self.running = False
            
        finally:
            # Clean up
            print("[Memory Load] Releasing memory...")
            self.memory_blocks.clear()
            print(f"[Memory Load] Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("[Memory Load] Memory released successfully")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate memory load for system performance testing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Allocate 500MB with sequential access for 60 seconds
  %(prog)s --size 500 --duration 60 --pattern sequential
  
  # Allocate 1GB with random access indefinitely
  %(prog)s --size 1024 --pattern random
  
  # Allocate 256MB with random access for 2 minutes
  %(prog)s --size 256 --duration 120 --pattern random
        """
    )
    
    parser.add_argument(
        '--size',
        type=int,
        default=100,
        help='Amount of memory to allocate in MB (default: 100)'
    )
    
    parser.add_argument(
        '--duration',
        type=int,
        default=0,
        help='Duration in seconds (0 = infinite, default: 0)'
    )
    
    parser.add_argument(
        '--pattern',
        type=str,
        choices=['sequential', 'random'],
        default='random',
        help='Memory access pattern (default: random)'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if args.size <= 0:
        print("Error: Size must be > 0")
        sys.exit(1)
        
    if args.duration < 0:
        print("Error: Duration must be >= 0")
        sys.exit(1)
        
    # Run the load generator
    generator = MemoryLoadGenerator(args.size, args.duration, args.pattern)
    generator.run()


if __name__ == '__main__':
    main()
