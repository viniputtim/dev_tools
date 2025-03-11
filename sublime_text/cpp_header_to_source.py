import os
import sys


class_name = ''
final_code = ''


def find_rel_path(file_path, include_dir):
    include_pos = file_path.find(include_dir)

    if include_pos != -1:
        rel_path = file_path[include_pos + len(include_dir):]
    else:
        rel_path = file_path

    return rel_path


def process_line(line):
    global class_name
    global final_code

    line = line.strip()

    if 'class ' in line:
        class_name = line.replace('class', '').strip()
    elif line.endswith(');'):
        words = line.split()
        return_type = ''
        body = ''
        is_body = False

        for word in words:
            if '(' in word:
                is_body = True
            if not(is_body):
                return_type += f'{word} '
            else:
                body += f'{word} '

        final_code += f'\n\n\n{return_type}{class_name}::{body.replace(";", "").strip()}\n'
        final_code += '{\n}'


def main():
    global final_code

    file_path = sys.argv[1]
    include_dir = 'include/'

    rel_path = find_rel_path(file_path, include_dir)
    final_code += f'# include "{rel_path}"'

    code_lines = []
    with open(file_path) as file:
        code_lines = file.readlines()

    for line in code_lines:
        process_line(line)

    print(final_code)


if __name__ == '__main__':
    main()
