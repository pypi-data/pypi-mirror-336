#!/usr/bin/env python3
import os
import sys
import subprocess
import webbrowser
from datetime import datetime, timedelta
import tempfile
import click
from pathlib import Path

def get_git_diff_since_date(days_ago):
    """Get git diff since specified days ago."""
    # Calculate the date
    target_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days_ago)
    date_str = target_date.strftime("%Y-%m-%d")
    
    # Get the git diff
    try:
        result = subprocess.run(
            ["git", "diff", f"--since={date_str}"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        click.echo(f"Error running git diff: {e}", err=True)
        sys.exit(1)

def create_html_diff(diff_content):
    """Create an HTML file with the diff content."""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Git Diff</title>
        <style>
            body {{
                font-family: monospace;
                line-height: 1.6;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            pre {{
                background-color: white;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .diff-add {{
                color: #28a745;
                background-color: #e6ffe6;
            }}
            .diff-remove {{
                color: #dc3545;
                background-color: #ffe6e6;
            }}
            .diff-header {{
                color: #6c757d;
                background-color: #f8f9fa;
            }}
        </style>
    </head>
    <body>
        <pre>{diff_content}</pre>
    </body>
    </html>
    """
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        return f.name

@click.command()
@click.argument('days', type=int)
def main(days):
    """Display git diffs in browser for the specified number of days."""
    if days < 1:
        click.echo("Days must be a positive number", err=True)
        sys.exit(1)
    
    # Get the git diff
    diff_content = get_git_diff_since_date(days)
    
    if not diff_content:
        click.echo("No changes found in the specified date range")
        sys.exit(0)
    
    # Create and open the HTML file
    html_file = create_html_diff(diff_content)
    webbrowser.open(f'file://{html_file}')
    click.echo(f"Opened diff in browser. HTML file saved at: {html_file}")

if __name__ == '__main__':
    main() 