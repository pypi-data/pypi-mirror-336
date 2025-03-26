"""
Core functionality for the pipup package.
"""

import os
import re
import subprocess
import concurrent.futures
from pathlib import Path


def get_latest_version(package_name):
    """Get the latest version of a package using pip index versions"""
    try:
        result = subprocess.run(
            ["pip", "index", "versions", package_name], 
            capture_output=True, 
            text=True, 
            check=True
        )
        output = result.stdout
        
        # Extract the latest version from the output
        latest_version_match = re.search(r"LATEST:\s+([0-9\.]+)", output)
        if latest_version_match:
            return latest_version_match.group(1)
            
        # Alternative pattern if LATEST is not present
        version_match = re.search(package_name + r"\s+\(([0-9\.]+)\)", output)
        if version_match:
            return version_match.group(1)
            
        return None
    except subprocess.CalledProcessError:
        print(f"Failed to get version for {package_name}")
        return None


def parse_requirements(file_path):
    """Parse a requirements.txt file and extract package info"""
    packages = []
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        # Skip comments and empty lines
        if not line or line.startswith('#'):
            packages.append((None, None, None, line))
            continue
            
        # Handle version specifiers (==, >=, <=, ~=, etc.)
        # Match exact version: package==1.2.3
        exact_match = re.match(r'([a-zA-Z0-9\-_\.]+)==([0-9\.]+)(.*)', line)
        if exact_match:
            package_name, current_version, comment = exact_match.groups()
            packages.append((package_name, current_version, "==", comment))
            continue
            
        # Match version range: package>=1.2.3
        range_match = re.match(r'([a-zA-Z0-9\-_\.]+)(>=|<=|~=|>|<)([0-9\.]+)(.*)', line)
        if range_match:
            package_name, operator, current_version, comment = range_match.groups()
            # Don't update packages with range specifications by default
            packages.append((package_name, current_version, operator, comment))
            continue
            
        # Any other format
        packages.append((None, None, None, line))
    
    return packages, lines


def update_requirements_file(file_path, parallel=True, max_workers=10, update_ranges=False, dry_run=False):
    """Update a requirements.txt file with the latest package versions"""
    if not file_path.exists():
        print(f"File {file_path} does not exist")
        return False
        
    print(f"Updating {file_path}")
    
    packages, lines = parse_requirements(file_path)
    
    # Only check exact version matches unless update_ranges is True
    package_names = [p[0] for p in packages if p[0] and (p[2] == "==" or update_ranges)]
    
    if not package_names:
        print(f"  No eligible packages to update in {file_path}")
        return False
    
    # Get latest versions (in parallel if enabled)
    latest_versions = {}
    if parallel and package_names:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_package = {
                executor.submit(get_latest_version, package): package 
                for package in package_names
            }
            for future in concurrent.futures.as_completed(future_to_package):
                package = future_to_package[future]
                try:
                    latest_versions[package] = future.result()
                except Exception as exc:
                    print(f"{package} generated an exception: {exc}")
    else:
        for package in package_names:
            latest_versions[package] = get_latest_version(package)
    
    # Generate updated file content
    updated_lines = []
    updates_made = False
    
    for package_name, current_version, operator, line_or_comment in packages:
        if package_name is None:
            # Comment or empty line
            updated_lines.append(line_or_comment + "\n")
            continue
        
        # Only update exact version matches unless update_ranges is True
        if operator != "==" and not update_ranges:
            updated_lines.append(f"{package_name}{operator}{current_version}{line_or_comment}\n")
            continue
            
        latest_version = latest_versions.get(package_name)
        
        if latest_version and latest_version != current_version:
            print(f"  Updating {package_name}: {current_version} -> {latest_version}")
            updated_lines.append(f"{package_name}{operator}{latest_version}{line_or_comment}\n")
            updates_made = True
        else:
            # No update needed
            updated_lines.append(f"{package_name}{operator}{current_version}{line_or_comment}\n")
    
    # Write updated file (unless dry run)
    if updates_made and not dry_run:
        with open(file_path, 'w') as f:
            f.writelines(updated_lines)
        print(f"✅ Updated {file_path}")
    elif updates_made:
        print(f"✓ Would update {file_path} (dry run)")
    else:
        print(f"✓ No updates needed for {file_path}")
    
    return updates_made


def find_requirements_files(directory='.', pattern='**/requirements.txt'):
    """Find requirements files in the given directory matching the pattern."""
    return list(Path(directory).glob(pattern))


def update_requirements_files(
    files=None, 
    directory='.', 
    pattern='**/requirements.txt',
    parallel=True, 
    max_workers=10, 
    update_ranges=False, 
    dry_run=False
):
    """Update multiple requirements files."""
    if files is None:
        files = find_requirements_files(directory, pattern)
    
    if not files:
        print(f"No requirements files found in {directory} matching {pattern}")
        return 0
        
    print(f"Found {len(files)} requirements files")
    if dry_run:
        print("Dry run mode - no changes will be made")
    
    # Update each file
    updates_count = 0
    for req_file in files:
        if update_requirements_file(req_file, parallel, max_workers, update_ranges, dry_run):
            updates_count += 1
    
    print(f"Updates completed: {updates_count} file(s) {'would be' if dry_run else ''} modified")
    return updates_count 