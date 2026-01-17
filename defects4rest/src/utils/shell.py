#-------------------------------------------------------------------------------
# Copyright (c) 2026 Rahil Piyush Mehta, Kausar Y. Moshood, Huwaida Rahman Yafie and Manish Motwani
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#-------------------------------------------------------------------------------

"""
Console output utilities for pretty-printing sections, steps, and command execution.

Provides colored terminal output with fallback for non-TTY environments.
"""
import subprocess
import shutil
import os
import sys

# ANSI color codes for terminal output
COLORS = {
    "reset": "\033[0m",
    "cyan": "\033[96m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "magenta": "\033[95m",
    "bold": "\033[1m",
    "red": "\033[91m",
}


def supports_color():
    """
    Check if the output terminal supports ANSI color codes.

    Returns:
        bool: True if stdout is a TTY (supports colors), False otherwise.
    """
    return sys.stdout.isatty()


def pretty_section(title: str, color: str = "cyan", char: str = "═"):
    """
    Print a prominent section header with colored borders.

    Creates a centered title surrounded by decorative lines that span
    the terminal width.

    Args:
        title: The section title text to display.
        color: Color name from COLORS dict (default: "cyan").
        char: Character to use for border lines (default: "═").
    """
    # Get terminal width (fallback to 80)
    width = shutil.get_terminal_size(fallback=(80, 20)).columns
    width = max(40, min(width, 120))  # clamp to reasonable range

    title = f"  {title.strip()}  "
    border_line = char * width

    if supports_color() and color in COLORS:
        c = COLORS[color]
        reset = COLORS["reset"]
        bold = COLORS["bold"]
        print()
        print(c + border_line + reset)
        print(c + (bold + title.center(width) + reset) + c.replace("\033[", "\033[0;"))  # safe-ish
        print(c + border_line + reset)
        print()
    else:
        # No color / non-TTY
        print()
        print(border_line)
        print(title.center(width))
        print(border_line)
        print()


def pretty_subsection(title: str, char: str = "-", pad: int = 2, width: int | None = None):
    """
    Print a smaller subsection header with decorative lines.

    Creates a centered title with padding, surrounded by character borders.

    Args:
        title: The subsection title text to display.
        char: Character to use for border (default: "-").
        pad: Padding spaces around title (default: 2).
        width: Optional fixed width, otherwise uses terminal width.
    """
    if width is None:
        width = shutil.get_terminal_size(fallback=(80, 20)).columns
        width = max(60, min(width, 140))  # clamp

    title = title.strip()
    label = (" " * pad) + title + (" " * pad)

    # If label is too long, just print it without borders
    if len(label) >= width:
        print(label)
        return

    # Calculate border lengths for left and right sides
    remaining = width - len(label)
    left = remaining // 2
    right = remaining - left
    print(char * left + label + char * right)


def pretty_step(msg: str, color: str = "green", prefix: str = "→"):
    """
    Print a single step/action line with colored prefix.

    Args:
        msg: The step message to display.
        color: Color name from COLORS dict (default: "green").
        prefix: Symbol to use as prefix (default: "→").
    """
    if supports_color():
        print(f"{COLORS[color]}{prefix}{COLORS['reset']} {msg}")
    else:
        print(f"{prefix} {msg}")


def run(cmd, env=None, cwd=None):
    """
    Execute a shell command and display output with pretty formatting.

    Runs the command, captures stdout/stderr, and displays them with
    colored formatting. Raises CalledProcessError if command fails.

    Args:
        cmd: List of command arguments (e.g., ["git", "clone", "url"]).
        env: Optional environment variables dict (defaults to os.environ).
        cwd: Optional working directory for command execution.
    """
    location = f"(cwd={cwd})" if cwd else ""
    pretty_step(f"cmd-> {' '.join(cmd)} {location}")

    # Execute command and capture output
    result = subprocess.run(
        cmd,
        env=env or os.environ,
        cwd=cwd,
        capture_output=True,
        text=True
    )

    # Display stdout in cyan if present
    if result.stdout:
        pretty_step(result.stdout, "cyan")

    # Display stderr in red if present
    if result.stderr:
        pretty_step(result.stderr, "red")

    # Raise exception if command failed
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)