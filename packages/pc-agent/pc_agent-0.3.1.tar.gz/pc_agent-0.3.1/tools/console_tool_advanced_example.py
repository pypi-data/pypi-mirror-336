#!/usr/bin/env python3
"""
Advanced example for using the ConsoleTool in an application.

This example demonstrates how to use the ConsoleTool for various system tasks:
- System information gathering
- Process management
- File operations
- Network diagnostics
"""
import os
import sys
import time
import platform
from typing import Dict, Any, List, Optional

from console_tool import ConsoleTool


class SystemHelper:
    """Helper class that uses ConsoleTool to perform system operations."""
    
    def __init__(self):
        """Initialize the SystemHelper with a ConsoleTool instance."""
        self.console = ConsoleTool()
        self.is_windows = platform.system() == "Windows"
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get basic system information."""
        if not self.is_windows:
            # Linux/macOS commands
            cpu_info = self.console.execute(command="cat /proc/cpuinfo | grep 'model name' | head -1")
            mem_info = self.console.execute(command="free -h")
            disk_info = self.console.execute(command="df -h")
            kernel_info = self.console.execute(command="uname -a")
        else:
            # Windows commands
            cpu_info = self.console.execute(command="wmic cpu get name")
            mem_info = self.console.execute(command="wmic OS get FreePhysicalMemory,TotalVisibleMemorySize")
            disk_info = self.console.execute(command="wmic logicaldisk get size,freespace,caption")
            kernel_info = self.console.execute(command="ver")
        
        return {
            "cpu": cpu_info["stdout"] if cpu_info["returncode"] == 0 else "Failed to retrieve CPU info",
            "memory": mem_info["stdout"] if mem_info["returncode"] == 0 else "Failed to retrieve memory info",
            "disk": disk_info["stdout"] if disk_info["returncode"] == 0 else "Failed to retrieve disk info",
            "kernel": kernel_info["stdout"] if kernel_info["returncode"] == 0 else "Failed to retrieve kernel info"
        }
    
    def list_running_processes(self, filter_term: Optional[str] = None) -> List[str]:
        """
        List running processes, optionally filtered by term.
        
        Args:
            filter_term: Optional term to filter processes by
            
        Returns:
            List of process names/details
        """
        if not self.is_windows:
            command = "ps aux"
            if filter_term:
                command += f" | grep {filter_term}"
        else:
            command = "tasklist"
            if filter_term:
                command += f" | findstr {filter_term}"
        
        result = self.console.execute(command=command)
        
        if result["returncode"] != 0:
            return []
        
        # Process the output into a list
        processes = result["stdout"].strip().split('\n')
        # Remove header line on non-Windows systems
        if not self.is_windows and len(processes) > 0 and "USER" in processes[0]:
            processes = processes[1:]
        
        return processes
    
    def check_network_connection(self, host: str = "8.8.8.8", count: int = 3) -> Dict[str, Any]:
        """
        Check network connection by pinging a host.
        
        Args:
            host: Host to ping
            count: Number of ping packets to send
            
        Returns:
            Dictionary with ping results
        """
        command = f"ping -c {count} {host}" if not self.is_windows else f"ping -n {count} {host}"
        result = self.console.execute(command=command)
        
        success = result["returncode"] == 0
        
        return {
            "success": success,
            "output": result["stdout"],
            "host": host,
            "packets_sent": count
        }
    
    def execute_task_with_progress(self, commands: List[str], 
                                  timeout: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Execute a series of commands with progress reporting.
        
        Args:
            commands: List of commands to execute
            timeout: Optional timeout for each command
            
        Returns:
            List of command execution results
        """
        results = []
        total_commands = len(commands)
        
        for i, command in enumerate(commands):
            print(f"Executing command {i+1}/{total_commands}: {command}")
            start_time = time.time()
            
            result = self.console.execute(command=command, timeout=timeout)
            
            execution_time = time.time() - start_time
            result["execution_time"] = execution_time
            
            print(f"Command completed in {execution_time:.2f} seconds with return code {result.get('returncode', 'N/A')}")
            results.append(result)
            
        return results


def main():
    """Run the advanced example."""
    helper = SystemHelper()
    
    print("\n===== SYSTEM INFORMATION =====")
    sys_info = helper.get_system_info()
    for key, value in sys_info.items():
        print(f"\n----- {key.upper()} -----")
        print(value)
    
    print("\n===== RUNNING PROCESSES =====")
    # List python-related processes
    python_processes = helper.list_running_processes("python")
    for process in python_processes[:5]:  # Show only first 5
        print(process)
    if len(python_processes) > 5:
        print(f"...and {len(python_processes) - 5} more")
    
    print("\n===== NETWORK CONNECTION =====")
    ping_result = helper.check_network_connection()
    print(f"Network connectivity: {'SUCCESSFUL' if ping_result['success'] else 'FAILED'}")
    
    print("\n===== TASK EXECUTION WITH PROGRESS =====")
    commands = [
        "echo 'Task 1: Creating a file' && touch /tmp/example_file.txt && sleep 1",
        "echo 'Task 2: Writing to the file' && echo 'Hello World' > /tmp/example_file.txt && sleep 1.5",
        "echo 'Task 3: Reading the file' && cat /tmp/example_file.txt && sleep 0.5",
        "echo 'Task 4: Removing the file' && rm /tmp/example_file.txt"
    ]
    # Use Windows-compatible commands if on Windows
    if platform.system() == "Windows":
        commands = [
            "echo Task 1: Creating a file && type nul > %TEMP%\\example_file.txt && timeout 1",
            "echo Task 2: Writing to the file && echo Hello World > %TEMP%\\example_file.txt && timeout 1.5",
            "echo Task 3: Reading the file && type %TEMP%\\example_file.txt && timeout 0.5",
            "echo Task 4: Removing the file && del %TEMP%\\example_file.txt"
        ]
    
    results = helper.execute_task_with_progress(commands)
    
    print("\n===== TASK RESULTS =====")
    for i, result in enumerate(results):
        print(f"\nTask {i+1}:")
        print(f"  Success: {result.get('returncode', 'N/A') == 0}")
        print(f"  Execution time: {result['execution_time']:.2f} seconds")
        # Truncate stdout if it's too long
        stdout = result.get('stdout', '')
        if len(stdout) > 100:
            stdout = stdout[:100] + "..."
        print(f"  Output: {stdout}")


if __name__ == "__main__":
    main() 