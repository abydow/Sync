import sys
import os
import importlib
import pytest

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

def test_load_database_service():
    module_name = "database.service"
    try:
        module = importlib.import_module(module_name)
        assert module is not None
    except ImportError as e:
        pytest.fail(f"Failed to import {module_name}: {e}")
