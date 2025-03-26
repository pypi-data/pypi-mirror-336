"""
IPython/Jupyter magic commands for copying code to clipboard.
"""
import pyperclip
from IPython.core.magic import Magics, magics_class, line_cell_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring


@magics_class
class ClipboardMagics(Magics):
    """Magics for copying code to the clipboard."""
    
    @line_cell_magic
    def clip(self, line, cell=None):
        """
        Copy line or cell content to the clipboard.
        
        Usage:
            %clip [line of code]  - copies the line to the clipboard
            %%clip                - copies the entire cell to the clipboard
        """
        if cell is not None:
            # This is cell mode
            content = cell
            message = f"Copied {len(content.splitlines())} lines to clipboard"
        else:
            # This is line mode
            content = line
            message = f"Copied to clipboard: {content}"
        
        if content:
            pyperclip.copy(content)
            print(message)
        else:
            print("No code to copy")


def load_ipython_extension(ipython):
    """
    Load the extension in IPython.
    
    This function is called when the extension is loaded.
    """
    ipython.register_magics(ClipboardMagics)