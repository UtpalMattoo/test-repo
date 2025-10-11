#!/usr/bin/env python3
"""
Test runner for server tests - handles path issues when running from repo root
"""
import sys
import os
import unittest

# Add server directory to Python path
server_dir = os.path.join(os.path.dirname(__file__), 'server')
if server_dir not in sys.path:
    sys.path.insert(0, server_dir)

if __name__ == '__main__':
    # Discover and run tests in the server directory
    loader = unittest.TestLoader()
    suite = loader.discover('server', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with error code if tests failed
    sys.exit(0 if result.wasSuccessful() else 1)