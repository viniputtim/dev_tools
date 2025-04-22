import os
import sys
import platform


includes = ['include', os.path.join('..', 'include')]
cpp_version = 'gnu++23'
test_folders = {'test', 'tests'}
source_folders = {'source', 'src'}


def to_snake(name):
    snake_name = name.lower()

    for char in [' ', '-']:
        snake_name = snake_name.replace(char, '_')

    return snake_name


def main():
    if len(sys.argv) < 2:
        print(f'Seriously? I only asked for 2 arguments. Are you lost?', file=sys.stderr)
        sys.exit(1)

    file_path = os.path.normpath(sys.argv[1])
    libraries = sys.argv[2].split(',') if len(sys.argv) > 2 else []

    if not os.path.basename(file_path) in source_folders:
        print(
            'Wrong folder, genius. Try running it from "source" like an actual developer.',
            file=sys.stderr
        )
        sys.exit(1)

    project_folder = os.path.abspath(os.path.join(file_path, '..'))

    project_name = os.path.basename(project_folder)
    file_name = to_snake(project_name)
    executable = os.path.join('..', 'bin', file_name)
    output_folder = os.path.dirname(executable)

    os.makedirs(output_folder, exist_ok=True)

    include_flags = ' '.join(f'-I "{x}"' for x in includes)
    compile_flags = f'-std={cpp_version}'
    link_flags = ''

    if 'raylib' in libraries:
        if platform.system() == 'Windows':
            link_flags += ' -lraylib -lopengl32 -lgdi32 -lwinmm'
        else:
            link_flags += ' -lraylib -lGL -lm -lpthread -ldl -lrt -lX11'

    source_files = []

    for root, _, files in os.walk(file_path):
        root_parts = root.split(os.sep)

        if any(test_dir in root_parts for test_dir in test_folders):
            continue

        for file in files:
            if file.endswith(('.c', '.cpp', '.cxx')):
                source_files.append(os.path.join(root, file))

    if not source_files:
        print('No source files found. Are you even trying?', file=sys.stderr)
        sys.exit(1)

    source_files_str = ' '.join(f'"{f}"' for f in source_files)
    cmd = f'g++ {compile_flags} -o "{executable}" {include_flags} {source_files_str} {link_flags}'

    print(cmd, flush=True)

    if os.system(cmd) == 0:
        os.system(f'"{executable}"')
    else:
        print('Compilation failed. Maybe you should check your code? Just a thought.', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
