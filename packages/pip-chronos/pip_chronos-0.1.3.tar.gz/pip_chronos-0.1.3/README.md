# pip-chronos

**pip-chronos** is a command-line tool that automatically updates your `requirements.txt` files with the latest package versions from PyPI. Like the Greek god Chronos who governs time, this tool helps keep your dependencies up to date.

## Features

- **Simple to Use**: Run with a single command to update all requirements
- **Parallel Processing**: Checks multiple packages concurrently for better performance
- **Flexible**: Update a specific file or search directories for requirements files
- **Version Constraint Awareness**: Handles all version specifiers (==, >=, <=, etc.)
- **Dry Run Mode**: Preview changes without modifying files
- **Smart Detection**: Preserves comments and formatting in requirements files

## Installation

Install from PyPI:

```bash
pip install pip-chronos
```

## Usage

Update all requirements files in the current directory and subdirectories:

```bash
pip-chronos
```

Update a specific requirements file:

```bash
pip-chronos path/to/requirements.txt
```

Run in dry-run mode (show changes without modifying files):

```bash
pip-chronos --dry-run
```

Exclude packages with version ranges (>=, <=, etc.):

```bash
pip-chronos --no-update-ranges
```

Use a custom pattern to find requirements files:

```bash
pip-chronos --pattern="**/requirements*.txt"
```

### Options

```
positional arguments:
  path                  Directory or specific requirements file path (default: current directory)

options:
  -h, --help            show this help message and exit
  --pattern PATTERN     Glob pattern for finding requirements files (default: **/requirements.txt)
  --sequential          Run updates sequentially (no parallel processing)
  --no-update-ranges    Do not update packages with range operators (>=, <=, etc.)
  --dry-run             Show what would be updated without making changes
  --max-workers MAX_WORKERS
                        Maximum number of worker threads (default: 10)
```

## Examples

Update all requirements files in the project:

```bash
pip-chronos
```

Update only a specific service subdirectory:

```bash
pip-chronos services/api-service/
```

Preview updates without making changes:

```bash
pip-chronos --dry-run
```

Exclude packages with version ranges (>=, <=, etc.):

```bash
pip-chronos --no-update-ranges
```

Use a custom pattern to find requirements files:

```bash
pip-chronos --pattern="**/requirements*.txt"
```

## How It Works

1. Finds all `requirements.txt` files in the specified directory (or uses a single file if provided)
2. For each package with a version specification, it checks for the latest available version using `pip index versions`
3. If a newer version is available, it updates the line in the requirements file
4. By default, all packages with version specifiers are updated
5. Preserves all comments and formatting in the requirements files

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 