"""
obutills - A collection of utility functions and tools for Python development
"""

__version__ = "0.1.0"

# Import utilities from modules to make them available at package level
from obutills.os import safe_system, safe_system_list

# File utilities
from obutills.files import (
    safe_mkdir,
    safe_remove,
    get_file_hash,
    safe_write_json,
    safe_read_json,
    find_files,
    TempFileContext
)

# Configuration utilities
from obutills.config import (
    ConfigManager,
    load_config,
    get_app_config_dir
)

# Logging utilities
from obutills.logging import (
    setup_logger,
    JsonFormatter,
    LogCapture,
    log_function_call
)
