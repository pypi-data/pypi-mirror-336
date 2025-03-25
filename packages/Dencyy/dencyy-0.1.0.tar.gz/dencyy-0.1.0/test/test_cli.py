import unittest
from pathlib import Path
import tempfile
import os
import sys

# Add the src directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from Dencyy.cli import scan_file, is_third_party

class TestReqGenerator(unittest.TestCase):
    def test_scan_file(self):
        # Create a temporary file with some imports
        with tempfile.NamedTemporaryFile(suffix='.py', mode='w+', delete=False) as f:
            f.write("""
import os
import sys
import requests
from pathlib import Path
from flask import Flask
import numpy as np
            """)
            temp_file = f.name
        
        try:
            # Test scanning the file
            imports = scan_file(temp_file)
            self.assertIn('os', imports)
            self.assertIn('sys', imports)
            self.assertIn('requests', imports)
            self.assertIn('pathlib', imports)
            self.assertIn('flask', imports)
            self.assertIn('numpy', imports)
        finally:
            # Clean up
            os.unlink(temp_file)
    
    def test_is_third_party(self):
        # Test standard library modules
        self.assertFalse(is_third_party('os'))
        self.assertFalse(is_third_party('sys'))
        self.assertFalse(is_third_party('pathlib'))
        
        # Test third-party modules
        self.assertTrue(is_third_party('requests'))
        self.assertTrue(is_third_party('flask'))
        self.assertTrue(is_third_party('numpy'))

if __name__ == '__main__':
    unittest.main()