'''
script to create docs
'''

import os
import pathlib
import re
import shutil
import subprocess
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
try:
    MODULE_NAME=eval([line for line in pathlib.Path('setup.py').read_text().splitlines() if line.startswith('MODULE =')][0].split('=')[1])
except Exception as ex:
    raise EnvironmentError(f"Unable to find module name from setup.py: {ex}")

if __name__ == '__main__':
    assert subprocess.call([
        sys.executable,
        '-m',
        'pip',
        'install',
        'setuptools',
        'pdoc3',
    ]) == 0, 'Unable to install pdoc3'

    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    assert subprocess.call([
        sys.executable,
        '-m',
        'pdoc',
        '--html',
        MODULE_NAME,
        '-o',
        'docs_tmp',
        '-f'
    ]) == 0, 'Unable to generate docs via pdoc'

    # remove existing docs dir
    shutil.rmtree('docs', ignore_errors=True)

    # remove extra dir nesting and move back to docs/
    shutil.move('docs_tmp/' + MODULE_NAME, 'docs')
    os.rmdir('docs_tmp')