#!/bin/bash
# Demo script for OS Performance Analyzer
# This script demonstrates various features of the toolkit

echo "=================================================================="
echo "       OS Performance Analyzer - Feature Demonstration"
echo "=================================================================="
echo

# Test 1: CPU Stress
echo "Test 1: CPU Stress Test"
echo "------------------------"
echo "Running CPU stress with 4 threads at 80% intensity for 10 seconds..."
python3 os_analyzer.py --cpu --cpu-intensity 0.8 --duration 10
echo
echo "Press Enter to continue to next test..."
read

# Test 2: Memory Stress - Linear Pattern
echo "Test 2: Memory Stress Test (Linear Pattern)"
echo "--------------------------------------------"
echo "Allocating 200MB of memory with linear pattern for 10 seconds..."
python3 os_analyzer.py --memory --memory-mb 200 --memory-pattern linear --duration 10
echo
echo "Press Enter to continue to next test..."
read

# Test 3: Memory Stress - Burst Pattern
echo "Test 3: Memory Stress Test (Burst Pattern)"
echo "-------------------------------------------"
echo "Allocating 300MB of memory with burst pattern for 10 seconds..."
python3 os_analyzer.py --memory --memory-mb 300 --memory-pattern burst --duration 10
echo
echo "Press Enter to continue to next test..."
read

# Test 4: Memory Stress - Wave Pattern
echo "Test 4: Memory Stress Test (Wave Pattern)"
echo "------------------------------------------"
echo "Allocating 200MB of memory with wave pattern for 15 seconds..."
python3 os_analyzer.py --memory --memory-mb 200 --memory-pattern wave --duration 15
echo
echo "Press Enter to continue to next test..."
read

# Test 5: Disk I/O - Sequential
echo "Test 5: Disk I/O Stress Test (Sequential)"
echo "------------------------------------------"
echo "Testing disk with 100MB sequential I/O for 10 seconds..."
python3 os_analyzer.py --disk --disk-mb 100 --disk-pattern sequential --duration 10
echo
echo "Press Enter to continue to next test..."
read

# Test 6: Disk I/O - Random
echo "Test 6: Disk I/O Stress Test (Random)"
echo "--------------------------------------"
echo "Testing disk with 50MB random I/O for 10 seconds..."
python3 os_analyzer.py --disk --disk-mb 50 --disk-pattern random --duration 10
echo
echo "Press Enter to continue to next test..."
read

# Test 7: Combined Stress
echo "Test 7: Combined Stress Test"
echo "-----------------------------"
echo "Running all stress tests simultaneously for 20 seconds..."
python3 os_analyzer.py --all --duration 20 --cpu-intensity 0.7 --memory-mb 300 --disk-mb 100
echo
echo "Press Enter to continue to final test..."
read

# Test 8: Full System Stress
echo "Test 8: Full System Stress Test"
echo "--------------------------------"
echo "Maximum stress test for 30 seconds..."
python3 os_analyzer.py --all --duration 30 --cpu-intensity 1.0 --memory-mb 500 --memory-pattern burst --disk-mb 200 --disk-pattern mixed
echo

echo "=================================================================="
echo "              Demonstration Complete!"
echo "=================================================================="
echo
echo "All tests completed successfully. The OS Performance Analyzer"
echo "provides comprehensive workload generation capabilities for:"
echo "  - CPU stress testing with configurable intensity"
echo "  - Memory allocation with multiple patterns"
echo "  - Disk I/O testing with various access patterns"
echo "  - Real-time system monitoring"
echo "  - Stability assessment and bottleneck detection"
echo
