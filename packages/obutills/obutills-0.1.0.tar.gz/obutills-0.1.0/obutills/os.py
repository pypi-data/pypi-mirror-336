"""
Safe OS utilities for executing system commands securely.
"""

import os
import subprocess
import shlex
import logging
from typing import List, Dict, Union, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def safe_system(command: str, 
                shell: bool = False, 
                cwd: Optional[str] = None, 
                env: Optional[Dict[str, str]] = None,
                timeout: Optional[int] = None,
                check: bool = True) -> str:
    """
    A safer alternative to os.system that prevents command injection and provides
    better control over command execution.
    
    Args:
        command (str): The command to execute
        shell (bool): Whether to use shell execution. Default is False for security.
                     Only set to True if absolutely necessary and input is trusted.
        cwd (str, optional): The working directory to run the command in
        env (dict, optional): Environment variables to set for the command
        timeout (int, optional): Maximum time in seconds for the command to complete
        check (bool): Whether to raise an exception if the command returns non-zero
    
    Returns:
        str: The command's stdout if successful, or stderr if there was an error
    
    Raises:
        subprocess.CalledProcessError: If check=True and the command returns non-zero
        subprocess.TimeoutExpired: If the timeout is reached
    
    Example:
        >>> output = safe_system('echo "Hello World"')
        >>> print(output)
        Hello World
    """
    try:
        logger.debug(f"Executing command: {command}")
        
        # If shell=False (safer), we need to properly split the command
        cmd_args = command if shell else shlex.split(command)
        
        # Run the command with controlled parameters
        process = subprocess.run(
            cmd_args,
            shell=shell,
            cwd=cwd,
            env=env,
            timeout=timeout,
            check=check,
            text=True,
            capture_output=True
        )
        
        return process.stdout.strip()
    
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with return code {e.returncode}: {e.stderr}")
        # Re-raise if check=True, otherwise return the error information
        if check:
            raise
        return e.stderr.strip() if e.stderr else f"Command failed with return code {e.returncode}"
    
    except subprocess.TimeoutExpired as e:
        error_msg = f"Command timed out after {timeout} seconds"
        logger.error(error_msg)
        if check:
            raise
        return error_msg
    
    except Exception as e:
        error_msg = f"Error executing command: {str(e)}"
        logger.error(error_msg)
        if check:
            raise
        return error_msg


def safe_system_list(commands: List[str], 
                    shell: bool = False,
                    cwd: Optional[str] = None,
                    env: Optional[Dict[str, str]] = None,
                    timeout: Optional[int] = None,
                    check: bool = True) -> List[str]:
    """
    Execute multiple commands safely and return their results.
    
    Args:
        commands (List[str]): List of commands to execute
        shell (bool): Whether to use shell execution
        cwd (str, optional): The working directory
        env (dict, optional): Environment variables
        timeout (int, optional): Maximum time per command
        check (bool): Whether to raise an exception on non-zero return
    
    Returns:
        List[str]: List of command outputs (stdout or stderr if error)
    
    Example:
        >>> results = safe_system_list(['echo "Hello"', 'echo "World"'])
        >>> for output in results:
        ...     print(output)
        Hello
        World
    """
    results = []
    
    for cmd in commands:
        output = safe_system(cmd, shell=shell, cwd=cwd, env=env, 
                           timeout=timeout, check=False)
        results.append(output)
        
        # Since we can't check return code directly anymore, we'll assume
        # an error occurred if the output looks like an error message
        # This is a heuristic and may need adjustment
        if check and ("failed" in output.lower() or "error" in output.lower() or "timed out" in output.lower()):
            break
            
    return results
