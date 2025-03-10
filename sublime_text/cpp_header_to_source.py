import os
import sys


# Inicialização de variáveis globais
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

    # Verifica se a linha contém a declaração de uma classe
    if 'class ' in line:
        class_name = line.replace('class', '').strip()
    # Verifica se a linha termina com ';' (indicando uma declaração de método)
    elif line.endswith(');'):
        words = line.split()
        return_type = ''
        body = ''
        is_body = False

        # Divide a linha em palavras e classifica como tipo e corpo
        for word in words:
            if '(' in word:
                is_body = True
            if not(is_body):
                return_type += f'{word} '
            else:
                body += f'{word} '

        # Adiciona o código da função ao final do código final
        final_code += f'\n\n\n{return_type}{class_name}::{body.replace(";", "").strip()}\n'
        final_code += '{\n}'


def main():
    global final_code

    # Pega o caminho do arquivo passado como argumento
    file_path = sys.argv[1]
    include_dir = 'include/'

    # Encontra o caminho relativo
    rel_path = find_rel_path(file_path, include_dir)

    # Inicializa a parte do include
    final_code += f'# include "{rel_path}"'

    # Lê as linhas do arquivo
    code_lines = []
    with open(file_path) as file:
        code_lines = file.readlines()

    # Processa cada linha do arquivo
    for line in code_lines:
        process_line(line)

    # Exibe o código gerado
    print(final_code)


if __name__ == '__main__':
    main()
