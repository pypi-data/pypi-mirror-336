"""
Command-line interface for the languagetools project.

On March 13th I vibe coded this to remove rich formatting from the error messages. It's surely not the cleanest implementation, and should probabluy be fixed.
"""
import typer.rich_utils
typer.rich_utils.STYLE_ERRORS = False

from typer import Typer
from typing import Any
import json
from .computer import Computer
import inspect
import click
import sys
from typer.core import TyperGroup
import io
from click.exceptions import ClickException
from click.core import ClickException, UsageError

class MinimalGroup(TyperGroup):
    def format_command_help(self, ctx, command, formatter):
        """Format help for a specific command"""
        # Get the command's help text
        help_text = command.help or command.callback.__doc__ or command.short_help or ""
        help_text = " ".join(help_text.split())
        
        # Write command usage
        formatter.write_text(f"Usage: {ctx.command_path} [OPTIONS]")
        
        # Write command description
        if help_text:
            formatter.write_text("\nDescription:")
            formatter.write_text(f"  {help_text}")
        
        # Write parameters if any
        params = command.get_params(ctx)
        if params:
            formatter.write_text("\nOptions:")
            for param in params:
                # Get parameter help
                param_help = param.help or ""
                param_help = " ".join(param_help.split())
                # Format parameter with its type and help
                type_str = param.type.name if hasattr(param.type, 'name') else str(param.type)
                formatter.write_text(f"  --{param.name} {type_str}")
                if param_help:
                    formatter.write_text(f"    {param_help}")
                formatter.write_text("")

    def get_command(self, ctx, cmd_name):
        cmd = super().get_command(ctx, cmd_name)
        if cmd is None:
            sys.stderr.write(f"Error: Unknown command '{cmd_name}'\nTry `lt --help` for help.\n")
            sys.exit(2)
        
        # Override the command's help formatting
        original_format_help = cmd.format_help
        def new_format_help(ctx, formatter):
            self.format_command_help(ctx, cmd, formatter)
        cmd.format_help = new_format_help
        
        return cmd

    def format_help(self, ctx, formatter):
        formatter.width = 80
        
        # Only show command names and their short help
        commands = self.list_commands(ctx)
        if commands:
            formatter.write_text("Commands:")
            for command in commands:
                cmd = self.get_command(ctx, command)
                if cmd is not None:
                    # Get help text from docstring or short_help
                    help_text = cmd.help or cmd.callback.__doc__ or cmd.short_help or ""
                    # Clean up the help text - remove extra whitespace and newlines
                    help_text = " ".join(help_text.split())
                    formatter.write_text(f"  {command}:")
                    if help_text:
                        formatter.write_text(f"    {help_text}")
                    formatter.write_text("")  # Add blank line between commands
        
        formatter.write_text("")

    def get_help(self, ctx):
        # Capture help text using StringIO
        out = io.StringIO()
        # Create formatter without the 'file' parameter
        formatter = click.HelpFormatter(width=80)
        self.format_help(ctx, formatter)
        # Write the formatted text to our StringIO object
        out.write(formatter.getvalue())
        return out.getvalue()

class MinimalClickCommand(click.Group):
    def format_usage(self, ctx, formatter):
        # Minimal usage format
        formatter.write_text(f"Usage: {ctx.command_path} [OPTIONS] COMMAND [ARGS]...")
    
    def get_help(self, ctx):
        # Get a list of available commands
        commands = sorted(self.list_commands(ctx))
        
        # Build a simple help text with just command names
        help_text = "Available commands: " + ", ".join(commands)
        return help_text

def custom_error_callback(ctx, exc):
    # Force print the error message
    print(f"Error: {str(exc)}", file=sys.stderr)
    sys.exit(1)

app = Typer(
    help="Command-line tool to interact with the languagetools suite.", 
    cls=MinimalGroup,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_enable=False
)

# Get the underlying Click command and add our error callback
click_command = app.command
if hasattr(click_command, '_click'):
    click_command._click.callback = custom_error_callback

# Create a single Computer instance
computer = Computer()

# Create sub-apps for each module, all using MinimalGroup
ai_app = Typer(help="AI functionalities", cls=MinimalGroup)
audio_app = Typer(help="Audio operations", cls=MinimalGroup)
browser_app = Typer(help="Browser automation", cls=MinimalGroup)
document_app = Typer(help="Document operations", cls=MinimalGroup)
files_app = Typer(help="File operations", cls=MinimalGroup)
vision_app = Typer(help="Vision and image operations", cls=MinimalGroup)
image_app = Typer(help="Image operations", cls=MinimalGroup)
video_app = Typer(help="Video operations", cls=MinimalGroup)

# Map modules to their respective Typer apps
MODULE_APPS = {
    "ai": ai_app,
    "audio": audio_app,
    "browser": browser_app,
    "document": document_app,
    "files": files_app,
    "vision": vision_app,
    "image": image_app,
    "audio": audio_app,
    "video": video_app,
}

# Add all sub-apps to the main app
for name, typer_app in MODULE_APPS.items():
    app.add_typer(typer_app, name=name)

### These are needed because many methods just return their result, and we want to print it

def print_result(result: Any) -> None:
    """Print the result in a readable format"""
    if result is None:
        return
    
    if isinstance(result, (dict, list)):
        # Pretty print JSON-serializable objects
        print(json.dumps(result, indent=2))
    else:
        print(result)

def create_wrapper(func):
    """Create a wrapper that handles any function signature"""
    func_name = func.__name__
    sig = inspect.signature(func)
    
    # Create a wrapper that accepts *args and **kwargs
    def wrapper(*args, **kwargs):
        # print(f"Calling {func.__name__} with args: {args} and kwargs: {kwargs}")
        if func_name == "cloud":
            tool = kwargs.get('tool')
            input_data = kwargs.get('input')
            tool_input = json.loads(input_data) if isinstance(input_data, str) else input_data
            result = func(tool, tool_input)
        else:
            result = func(*args, **kwargs)
        print_result(result)
        return result
    
    # Copy the signature and metadata to the wrapper
    wrapper.__signature__ = sig
    wrapper.__doc__ = func.__doc__
    wrapper.__annotations__ = func.__annotations__
    return wrapper

# Automatically create CLI commands from the Computer class methods
for module_name, typer_app in MODULE_APPS.items():
    module = getattr(computer, module_name)
    for method_name in dir(module):
        if not method_name.startswith('_'):  # Skip private methods
            method = getattr(module, method_name)
            if callable(method):
                wrapped_method = create_wrapper(method)
                typer_app.command(method_name)(wrapped_method)

def main():
    # Store both the original stderr object and its write function
    original_stderr = sys.stderr
    original_stderr_write = sys.stderr.write
    
    def minimal_stderr_write(text):
        return original_stderr_write(text)
    
    class MinimalStderr:
        def write(self, text):
            return minimal_stderr_write(text)
        
        def flush(self):
            # Use the original stderr object for flush
            original_stderr.flush()
    
    # Replace stderr with our minimal version
    sys.stderr = MinimalStderr()
    
    try:
        app()
    except Exception as e:
        sys.stderr.write(f"{str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()