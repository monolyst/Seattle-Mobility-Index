import sys
import os
DIRECTORIES = ['core', 'analysis', 'preproc', 'tests']
scripts_dir = os.path.abspath(os.curdir)
for directory in DIRECTORIES:
    new_dir = os.path.join(scripts_dir, directory)
    sys.path.insert(0, new_dir)
