"""Tests for the updater module."""

import os
import tempfile
from pathlib import Path

import pytest

from pipup.updater import parse_requirements, update_requirements_file


def test_parse_requirements():
    """Test parsing a requirements.txt file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("# Comment line\n")
        f.write("package1==1.0.0  # Comment\n")
        f.write("package2>=2.0.0\n")
        f.write("\n")
        f.write("package3~=3.0.0\n")
        file_path = f.name

    try:
        packages, lines = parse_requirements(Path(file_path))
        
        assert len(packages) == 5
        assert packages[0] == (None, None, None, "# Comment line")
        assert packages[1] == ("package1", "1.0.0", "==", "  # Comment")
        assert packages[2] == ("package2", "2.0.0", ">=", "")
        assert packages[3] == (None, None, None, "")
        assert packages[4] == ("package3", "3.0.0", "~=", "")
        
        assert len(lines) == 5
    finally:
        os.unlink(file_path)


def test_update_requirements_file(mocker):
    """Test updating a requirements.txt file."""
    # Mock get_latest_version to return predictable values
    mocker.patch(
        'pipup.updater.get_latest_version',
        side_effect=lambda pkg: {"package1": "2.0.0", "package2": "3.0.0"}.get(pkg, None)
    )
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("# Comment line\n")
        f.write("package1==1.0.0  # Comment\n")
        f.write("package2>=2.0.0\n")
        file_path = f.name
    
    try:
        # Test dry-run mode
        updated = update_requirements_file(Path(file_path), dry_run=True)
        assert updated is True
        
        # Verify content wasn't changed
        with open(file_path, 'r') as f:
            content = f.read()
        assert "package1==1.0.0" in content
        
        # Test actual update
        updated = update_requirements_file(Path(file_path), update_ranges=True)
        assert updated is True
        
        # Verify content was updated
        with open(file_path, 'r') as f:
            content = f.read()
        assert "package1==2.0.0" in content
        assert "package2>=3.0.0" in content
    finally:
        os.unlink(file_path) 