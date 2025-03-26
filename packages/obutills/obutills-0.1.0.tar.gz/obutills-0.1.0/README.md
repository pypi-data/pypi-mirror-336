# obutills

A collection of utility functions and tools for Python development.

## Installation

```bash
pip install obutills
```

## Features

- **Safe System Commands**: Execute system commands safely with `safe_system`
- **File Utilities**: Safely manage files with utilities like `safe_mkdir`, `safe_remove`, etc.
- **Configuration Management**: Handle application configuration with `ConfigManager`
- **Logging Utilities**: Set up logging easily with `setup_logger`

## Usage Examples

### Safe System Commands

```python
from obutills import safe_system

# Execute a command and get the output
output = safe_system("echo Hello World")
print(output)  # Prints: Hello World

# With more options
output = safe_system("ls -la", cwd="/tmp", timeout=5)
```

### File Utilities

```python
from obutills import safe_mkdir, safe_remove, safe_read_json, safe_write_json

# Create directories safely
safe_mkdir("/path/to/directory")

# Write and read JSON
data = {"key": "value"}
safe_write_json("/path/to/file.json", data)
loaded_data = safe_read_json("/path/to/file.json")

# Use temporary files
from obutills import TempFileContext

with TempFileContext() as tmp:
    tmp_file = tmp.create_file(content="test data")
    # Use tmp_file...
# File is automatically deleted when context exits
```

### Configuration Management

```python
from obutills import ConfigManager, get_app_config_dir

# Get platform-specific config directory
config_dir = get_app_config_dir("myapp")

# Load configuration from file with environment variable overrides
config = ConfigManager("config.yaml", env_prefix="MYAPP_")

# Access configuration values
database_url = config.get("database.url", "default_url")
debug_mode = config.get("debug", False)

# Set and save configuration
config.set("logging.level", "DEBUG")
config.save()
```

### Logging Utilities

```python
from obutills import setup_logger, log_function_call

# Set up a logger with file and console output
logger = setup_logger(
    name="myapp",
    level="INFO",
    log_file="/path/to/app.log",
    json_format=False
)

# Use decorator to log function calls
@log_function_call()
def add(a, b):
    return a + b

result = add(1, 2)  # Logs function call and result
```

## License

MIT License
