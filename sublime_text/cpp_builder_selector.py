import os
import sys


packages_dir = '/home/viniciuspm/.config/sublime-text/Packages/User'


if sys.argv[1].endswith('.h') or sys.argv[1].endswith('.hpp'):
    os.system(f'python3 "{packages_dir}/cpp_header_to_source.py" {sys.argv[1]}')
else:
    os.system(
        f'python3 "{packages_dir}/cpp_builder.py" {sys.argv[1]} {sys.argv[2]} {sys.argv[3]}'
    )