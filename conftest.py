"""Ensure the repo root is importable for the test suite."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
