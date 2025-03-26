"""
Command-line interface for pipup.
"""

import argparse
from pathlib import Path
from .updater import update_requirements_files, find_requirements_files


def main():
    """Main entry point for the pipup CLI."""
    parser = argparse.ArgumentParser(
        description='Update requirements.txt files with latest package versions.'
    )
    
    # Basic options
    parser.add_argument(
        'path', 
        nargs='?', 
        type=str, 
        default='.',
        help='Directory or specific requirements file path (default: current directory)'
    )
    
    # Options
    parser.add_argument(
        '--pattern', 
        type=str, 
        default='**/requirements.txt',
        help='Glob pattern for finding requirements files (default: **/requirements.txt)'
    )
    parser.add_argument(
        '--sequential', 
        action='store_true',
        help='Run updates sequentially (no parallel processing)'
    )
    parser.add_argument(
        '--no-update-ranges', 
        action='store_true',
        dest='no_update_ranges',
        default=False,
        help='Do not update packages with range operators (>=, <=, etc.)'
    )
    parser.add_argument(
        '--no-validate', 
        action='store_true',
        dest='no_validate',
        default=False,
        help='Skip validation of dependencies'
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true',
        help='Show what would be updated without making changes'
    )
    parser.add_argument(
        '--max-workers', 
        type=int, 
        default=10,
        help='Maximum number of worker threads (default: 10)'
    )
    
    args = parser.parse_args()
    
    # Determine if path is a specific file or a directory to search
    path = Path(args.path)
    
    if path.is_file() and path.name.endswith('.txt'):
        # Update a single file
        files = [path]
    else:
        # Find files based on pattern
        files = find_requirements_files(directory=path, pattern=args.pattern)
    
    # Update the files
    update_requirements_files(
        files=files,
        parallel=not args.sequential,
        max_workers=args.max_workers,
        update_ranges=not args.no_update_ranges,
        dry_run=args.dry_run,
        validate=not args.no_validate
    )


if __name__ == '__main__':
    main() 