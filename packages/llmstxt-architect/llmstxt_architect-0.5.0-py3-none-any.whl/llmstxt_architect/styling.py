"""
Styling utilities for terminal output.
"""

from typing import Dict, List, Any

# ANSI escape codes for colors
COLORS = {
    "green": "\033[92m",
    "cyan": "\033[96m",
    "magenta": "\033[95m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}


def color_text(text: str, color: str) -> str:
    """
    Add color to terminal text.
    
    Args:
        text: The text to color
        color: The color to use
    
    Returns:
        The colored text
    """
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"

def draw_box(text: str, color: str = "green", padding: int = 1) -> str:
    """
    Draw a box around text in the terminal.
    
    Args:
        text: The text to put in the box
        color: The color to use for the box
        padding: Padding inside the box
    
    Returns:
        The boxed text
    """
    lines = text.split('\n')
    width = max(len(line) for line in lines)
    
    horizontal_border = '┌' + '─' * (width + padding * 2) + '┐'
    empty_line = '│' + ' ' * (width + padding * 2) + '│'
    
    result = [color_text(horizontal_border, color)]
    
    for _ in range(padding):
        result.append(color_text(empty_line, color))
    
    for line in lines:
        padded_line = line.ljust(width)
        result.append(color_text(f'│{" " * padding}{padded_line}{" " * padding}│', color))
    
    for _ in range(padding):
        result.append(color_text(empty_line, color))
    
    result.append(color_text('└' + '─' * (width + padding * 2) + '┘', color))
    
    return '\n'.join(result)

def status_message(message: str, status: str = "info") -> str:
    """
    Format a status message with appropriate color.
    
    Args:
        message: The message to display
        status: The status type (info, success, error, warning)
    
    Returns:
        The formatted status message
    """
    status_colors = {
        "info": "cyan",
        "success": "green",
        "error": "red",
        "warning": "yellow",
        "processing": "magenta"
    }
    
    color = status_colors.get(status, "cyan")
    status_upper = status.upper()
    
    return f"{color_text('[' + status_upper + ']', color)} {message}"

def generate_summary_report(stats: Dict[str, Any]) -> str:
    """
    Generate a summary report of the processing.
    
    Args:
        stats: Dictionary containing statistics about the processing
    
    Returns:
        Formatted summary report
    """
    report = [
        f"✅ URLs Processed: {stats.get('urls_processed', 0)}",
        f"📄 Summaries Generated: {stats.get('summaries_generated', 0)}",
        f"⏱️ Total Time: {stats.get('total_time', 0):.2f}s",
        f"💾 Output: {stats.get('output_path', 'N/A')}"
    ]
    
    if stats.get('failed_urls'):
        report.append(f"❌ Failed URLs: {len(stats.get('failed_urls', []))}")
    
    return draw_box('\n'.join(report), "green", 2)