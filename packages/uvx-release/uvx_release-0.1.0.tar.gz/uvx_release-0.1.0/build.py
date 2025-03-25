#!/usr/bin/env python3
"""
Command line wrapper to run `uv build` after cleaning the `dist/` directory.
"""

import subprocess
import shutil
from pathlib import Path
import sys

def main() -> int:
    rest = sys.argv[1:] # For passing additional arguments to `uv build`
    dist_dir = Path('dist')
    if dist_dir.exists() and dist_dir.is_dir():
        print('Cleaning dist/ directory...')
        shutil.rmtree(dist_dir)

    print('Running `uv build`...')
    result = subprocess.run(['uv', 'build'] + rest)
    return result.returncode

if __name__ == '__main__':
    sys.exit(main())
