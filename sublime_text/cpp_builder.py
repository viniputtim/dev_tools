import os
import sys


file_name = sys.argv[1]
file_folder = sys.argv[2]
libraries = sys.argv[3]

file_first_name = os.path.splitext(os.path.basename(file_name))[0]
cpp_files = []
flags = ''
executable = os.path.join('..', 'bin', file_first_name)
output_folder = os.path.dirname(executable)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

if 'raylib' in libraries:
    flags += '-lraylib -lGL -lm -lpthread -ldl -lrt -lX11'

for root, folders, files in os.walk(file_folder):
    for file in files:
        if file.endswith('.c') or file.endswith('.cpp'):
            cpp_files.append(os.path.join(root, file))

cmd = f'g++ -std=gnu++23 -o {executable} -I "include" {" ".join(cpp_files)} {flags}'

os.system(cmd)
os.system(executable)