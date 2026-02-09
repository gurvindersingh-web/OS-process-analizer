"""Configuration management for OS Performance Analyzer."""
import json
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class WorkloadConfig:
    """Configuration for workload generation."""
    # CPU Configuration
    cpu_enabled: bool = True
    cpu_threads: int = 1
    cpu_intensity: float = 50.0  # Percentage (0-100)
    cpu_duration: int = 60  # seconds
    
    # Memory Configuration
    memory_enabled: bool = True
    memory_size_mb: int = 100  # MB to allocate
    memory_pattern: str = "sequential"  # sequential, random
    memory_duration: int = 60  # seconds
    
    # Disk I/O Configuration
    disk_enabled: bool = True
    disk_file_size_mb: int = 10  # MB per file
    disk_num_files: int = 5
    disk_pattern: str = "sequential"  # sequential, random
    disk_duration: int = 60  # seconds
    disk_work_dir: str = "/tmp/os_analyzer"
    
    # Monitoring Configuration
    monitoring_interval: float = 1.0  # seconds
    display_realtime: bool = True
    
    def to_json(self, filename: str):
        """Save configuration to JSON file."""
        with open(filename, 'w') as f:
            json.dump(asdict(self), f, indent=2)
    
    @classmethod
    def from_json(cls, filename: str) -> 'WorkloadConfig':
        """Load configuration from JSON file."""
        with open(filename, 'r') as f:
            data = json.load(f)
        return cls(**data)


# Predefined load patterns
LOAD_PATTERNS = {
    "light": WorkloadConfig(
        cpu_intensity=25.0,
        cpu_threads=1,
        memory_size_mb=50,
        disk_file_size_mb=5,
        disk_num_files=3,
    ),
    "moderate": WorkloadConfig(
        cpu_intensity=50.0,
        cpu_threads=2,
        memory_size_mb=100,
        disk_file_size_mb=10,
        disk_num_files=5,
    ),
    "heavy": WorkloadConfig(
        cpu_intensity=75.0,
        cpu_threads=4,
        memory_size_mb=200,
        disk_file_size_mb=20,
        disk_num_files=10,
    ),
    "extreme": WorkloadConfig(
        cpu_intensity=90.0,
        cpu_threads=8,
        memory_size_mb=500,
        disk_file_size_mb=50,
        disk_num_files=20,
    ),
}


def get_preset_config(preset: str) -> Optional[WorkloadConfig]:
    """Get a predefined configuration by name."""
    return LOAD_PATTERNS.get(preset)
