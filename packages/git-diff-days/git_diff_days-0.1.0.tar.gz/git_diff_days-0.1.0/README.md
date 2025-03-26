# Git Diff Days

A command-line tool that displays git diffs in your browser for a specified date range.

## Installation

You can install this package using pip:

```bash
pip install git-diff-days
```

## Usage

Run the command in any git repository:

```bash
gitdiffdays <days>
```

Where `<days>` is the number of days to look back. For example:
- `gitdiffdays 1` will show all changes since today at 00:00
- `gitdiffdays 2` will show all changes since yesterday at 00:00
- `gitdiffdays 7` will show all changes in the last week

The tool will automatically open your default web browser with a nicely formatted view of the git diff.

## Features

- Shows git diffs in a clean, browser-based interface
- Color-coded additions and removals
- Monospace font for better readability
- Responsive design that works on all screen sizes 