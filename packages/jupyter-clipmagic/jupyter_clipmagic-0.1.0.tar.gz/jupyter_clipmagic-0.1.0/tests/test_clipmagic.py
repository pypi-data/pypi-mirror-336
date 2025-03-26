"""
Tests for the jupyter_clipmagic extension.
"""
import pytest
from unittest.mock import patch
import pyperclip
from IPython.testing.globalipapp import get_ipython
from jupyter_clipmagic.clipmagic import ClipboardMagics, load_ipython_extension


class TestClipboardMagics:
    
    @classmethod
    def setup_class(cls):
        # Get the global IPython instance
        cls.ip = get_ipython()
        if cls.ip is None:
            pytest.skip("IPython environment not available")
        
        # Load our extension
        load_ipython_extension(cls.ip)
    
    @patch('pyperclip.copy')
    def test_line_magic(self, mock_copy):
        """Test the line magic."""
        # Run the line magic
        code = "print('Hello, world!')"
        self.ip.run_line_magic("clip", code)
        
        # Verify that pyperclip.copy was called with the expected text
        mock_copy.assert_called_once_with(code)
    
    @patch('pyperclip.copy')
    def test_cell_magic(self, mock_copy):
        """Test the cell magic."""
        # Run the cell magic
        cell_code = "for i in range(10):\n    print(i)"
        self.ip.run_cell_magic("clip", "", cell_code)
        
        # Verify that pyperclip.copy was called with the expected text
        mock_copy.assert_called_once_with(cell_code)