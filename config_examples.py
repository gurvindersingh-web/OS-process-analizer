# OS Performance Analyzer - Example Configuration
# This file demonstrates how to configure the analyzer programmatically

# Example configuration dictionary format
example_config = {
    # General settings
    'duration': 60.0,  # Test duration in seconds
    
    # CPU stress test settings
    'cpu_stress': True,
    'cpu_threads': None,  # None = use all CPU cores, or specify a number
    'cpu_intensity': 0.8,  # 0.0 to 1.0, where 1.0 is maximum load
    
    # Memory stress test settings
    'memory_stress': True,
    'memory_mb': 500,  # Target memory allocation in MB
    'memory_pattern': 'linear',  # Options: 'linear', 'burst', 'wave'
    
    # Disk I/O stress test settings
    'disk_stress': True,
    'disk_mb': 100,  # Data size for disk operations in MB
    'disk_pattern': 'sequential',  # Options: 'sequential', 'random', 'mixed'
}

# Preset configurations for common scenarios

# Light stress test - suitable for monitoring without overloading
light_stress = {
    'duration': 30.0,
    'cpu_stress': True,
    'cpu_intensity': 0.3,
    'memory_stress': True,
    'memory_mb': 100,
    'memory_pattern': 'linear',
    'disk_stress': False,
}

# CPU intensive test - focus on CPU performance
cpu_intensive = {
    'duration': 60.0,
    'cpu_stress': True,
    'cpu_threads': None,  # Use all cores
    'cpu_intensity': 1.0,  # Maximum load
    'memory_stress': False,
    'disk_stress': False,
}

# Memory intensive test - focus on memory allocation patterns
memory_intensive = {
    'duration': 45.0,
    'cpu_stress': False,
    'memory_stress': True,
    'memory_mb': 1000,
    'memory_pattern': 'wave',
    'disk_stress': False,
}

# Disk I/O intensive test - focus on disk operations
disk_intensive = {
    'duration': 60.0,
    'cpu_stress': False,
    'memory_stress': False,
    'disk_stress': True,
    'disk_mb': 500,
    'disk_pattern': 'mixed',
}

# Full system stress - all components at high load
full_system_stress = {
    'duration': 120.0,
    'cpu_stress': True,
    'cpu_threads': None,
    'cpu_intensity': 0.9,
    'memory_stress': True,
    'memory_mb': 1000,
    'memory_pattern': 'burst',
    'disk_stress': True,
    'disk_mb': 200,
    'disk_pattern': 'mixed',
}

# Stability test - moderate sustained load
stability_test = {
    'duration': 300.0,  # 5 minutes
    'cpu_stress': True,
    'cpu_intensity': 0.5,
    'memory_stress': True,
    'memory_mb': 500,
    'memory_pattern': 'linear',
    'disk_stress': True,
    'disk_mb': 100,
    'disk_pattern': 'sequential',
}
