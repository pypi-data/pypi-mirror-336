"""
File-related utilities for Python applications.
"""

import os
import shutil
import tempfile
import hashlib
import json
from typing import List, Dict, Any, Optional, Union, BinaryIO, TextIO, Iterator
from pathlib import Path


def safe_mkdir(directory: str, mode: int = 0o777, exist_ok: bool = True) -> str:
    """
    Safely create a directory and all parent directories.
    
    Args:
        directory (str): Path to the directory to create
        mode (int): Permission bits (octal)
        exist_ok (bool): If False, raise an error if directory exists
        
    Returns:
        str: Path to the created directory
        
    Raises:
        FileExistsError: If directory exists and exist_ok is False
    """
    os.makedirs(directory, mode=mode, exist_ok=exist_ok)
    return directory


def safe_remove(path: str, missing_ok: bool = True) -> bool:
    """
    Safely remove a file or directory.
    
    Args:
        path (str): Path to remove
        missing_ok (bool): If True, don't raise an error if the path doesn't exist
        
    Returns:
        bool: True if removal was successful, False if path didn't exist and missing_ok=True
        
    Raises:
        FileNotFoundError: If path doesn't exist and missing_ok=False
    """
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        return True
    except FileNotFoundError:
        if missing_ok:
            return False
        raise


def get_file_hash(file_path: str, algorithm: str = 'sha256', buffer_size: int = 65536) -> str:
    """
    Calculate the hash of a file.
    
    Args:
        file_path (str): Path to the file
        algorithm (str): Hash algorithm to use ('md5', 'sha1', 'sha256', etc.)
        buffer_size (int): Size of chunks to read
        
    Returns:
        str: Hexadecimal digest of the file
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If algorithm is not supported
    """
    hash_func = getattr(hashlib, algorithm, None)
    if not hash_func:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    
    file_hash = hash_func()
    with open(file_path, 'rb') as f:
        while chunk := f.read(buffer_size):
            file_hash.update(chunk)
    
    return file_hash.hexdigest()


def safe_write_json(file_path: str, data: Union[Dict, List], indent: int = 4, 
                   ensure_ascii: bool = False, sort_keys: bool = False) -> None:
    """
    Safely write JSON data to a file (creates parent directories if needed).
    
    Args:
        file_path (str): Path to the file
        data (dict or list): Data to write
        indent (int): Number of spaces for indentation
        ensure_ascii (bool): If True, escape non-ASCII characters
        sort_keys (bool): If True, sort dictionary keys
        
    Raises:
        TypeError: If data is not JSON serializable
    """
    directory = os.path.dirname(file_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii, sort_keys=sort_keys)


def safe_read_json(file_path: str, default: Any = None) -> Union[Dict, List, Any]:
    """
    Safely read JSON data from a file.
    
    Args:
        file_path (str): Path to the file
        default: Value to return if file doesn't exist or isn't valid JSON
        
    Returns:
        The parsed JSON data or the default value
        
    Raises:
        json.JSONDecodeError: If file contains invalid JSON and no default is provided
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        if default is not None:
            return default
        raise


def find_files(directory: str, pattern: str = "*", recursive: bool = True) -> List[str]:
    """
    Find files matching a pattern in a directory.
    
    Args:
        directory (str): Directory to search in
        pattern (str): Glob pattern to match
        recursive (bool): Whether to search recursively
        
    Returns:
        List[str]: List of matching file paths
    """
    return [str(p) for p in Path(directory).glob(pattern if not recursive else f"**/{pattern}")]


class TempFileContext:
    """
    Context manager for creating and automatically cleaning up temporary files.
    
    Example:
        >>> with TempFileContext() as tmp:
        >>>     tmp_file = tmp.create_file(content="test data")
        >>>     # Use tmp_file...
        >>> # File is automatically deleted when context exits
    """
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        Initialize the temporary file context.
        
        Args:
            base_dir (str, optional): Base directory for temporary files
        """
        self.base_dir = base_dir
        self.temp_dir = None
        self.files = []
    
    def __enter__(self):
        self.temp_dir = tempfile.mkdtemp(dir=self.base_dir)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
    
    def create_file(self, content: Optional[Union[str, bytes]] = None, 
                   suffix: str = "", prefix: str = "tmp", binary: bool = False) -> str:
        """
        Create a temporary file within the context.
        
        Args:
            content: Content to write to the file
            suffix (str): File suffix
            prefix (str): File prefix
            binary (bool): Whether to open the file in binary mode
            
        Returns:
            str: Path to the created temporary file
        """
        mode = 'wb' if binary or isinstance(content, bytes) else 'w'
        fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=self.temp_dir)
        
        try:
            if content is not None:
                with open(fd, mode) as f:
                    f.write(content)
            else:
                os.close(fd)
        except:
            os.close(fd)
            raise
            
        self.files.append(path)
        return path
    
    def cleanup(self):
        """Remove all temporary files and the temporary directory."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None
            self.files = []
