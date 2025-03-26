from setuptools import setup, find_packages

setup(
    name="git-diff-days",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "gitdiffdays=git_diff_days.cli:main",
        ],
    },
    author="Rudolf Cicko",
    description="A tool to view git diffs in browser for a specified date range",
    python_requires=">=3.6",
) 