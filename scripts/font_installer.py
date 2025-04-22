import os
import re
import shutil
import zipfile


GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'


class FontInstaller:
    def __init__(self):
        self.zip_path = '/home/viniciuspm/Downloads'
        self.extract_path = os.path.join(self.zip_path, 'fonts')
        self.project_path = '/home/viniciuspm/Desenvolvimento/its_about_cards'
        self.fonts_path = os.path.join(self.project_path, 'resources/fonts')
        self.licenses_path = os.path.join(self.project_path, 'docs/LICENSES')
        self.fonts_list_path = os.path.join(self.project_path, 'source/data/fonts_list.cpp')


    def to_snake_case(self, name):
        name = re.sub(r'[\s\-]+', '_', name)
        name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)

        return name.lower().strip()


    def to_natural_case(self, name):
        name = re.sub(r'[_\-]+', ' ', name)
        name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)

        return name.lower().strip()


    def extract_fonts(self):
        for file in os.listdir(self.zip_path):
            if file.endswith('.zip'):
                zip_path = os.path.join(self.zip_path, file)

                if ',' in zip_path:
                    extract_folder = self.extract_path
                else:
                    extract_folder = os.path.join(self.extract_path, os.path.splitext(file)[0])

                with zipfile.ZipFile(zip_path, 'r') as zip_file:
                    zip_file.extractall(extract_folder)


    def install_font(self):
        self.extract_fonts()

        if os.path.exists(self.extract_path):
            installed_fonts = self.process_fonts()
            self.list_fonts()

            print(f'{GREEN}{installed_fonts} installed with success!{RESET}\n\n')
        else:
            print(F'{RED}empty folder!{RESET}\n\n')

        self.run()


    def process_fonts(self):
        installed_fonts = ''
        i = 0

        for folder in os.listdir(self.extract_path):
            folder_path = os.path.join(self.extract_path, folder)

            if os.path.isdir(folder_path):
                self.process_folder(folder_path)

            current_font = self.to_natural_case(folder)

            if i == 0:
                conjunction = ''
            elif i == 1:
                conjunction = ' and '
            else:
                conjunction = ', '

            installed_fonts = f'{current_font}{conjunction}{installed_fonts}'
            i += 1

        return installed_fonts


    def process_folder(self, folder):
        folder_name = os.path.basename(folder)
        snake_name = self.to_snake_case(folder_name)
        dest_folder = os.path.join(self.fonts_path, folder_name)

        for file in os.listdir(folder):
            if file == 'OFL.txt' or file == 'LICENSE.txt':
                file_path = os.path.join(folder, file)
                license_dest_folder = os.path.join(self.licenses_path, snake_name)
                license_dest_file = os.path.join(license_dest_folder, file)

                os.makedirs(license_dest_folder, exist_ok = True)
                shutil.move(file_path, license_dest_file)

        if os.path.exists(dest_folder):
            shutil.rmtree(dest_folder)

        shutil.move(folder, dest_folder)


    def list_fonts(self):
        content = []

        for root, dirs, files in os.walk(self.fonts_path):
            for file in files:
                if file.endswith('.ttf'):
                    key = os.path.splitext(file)[0]
                    key = self.to_natural_case(key)
                    path = os.path.join(root, file)
                    path = path.replace(self.project_path, '..')

                    line = f'    {{"{key}", "{path}"}},'
                    content.append(line)

        self.update_fonts_list(content)


    def update_fonts_list(self, entries):
        with open(self.fonts_list_path, 'r') as f:
            lines = f.readlines()

        insert_index = max(0, len(lines) - 1)

        while insert_index > 0 and not lines[insert_index].strip().endswith('};'):
            insert_index -= 1

        for entry in reversed(entries):
            entry_line = f'{entry} \n'

            if entry_line not in lines:
                lines.insert(insert_index, entry_line)

        with open(self.fonts_list_path, 'w') as f:
            f.writelines(lines)


    def uninstall_font(self, font_folder_name):
        font_name = self.to_natural_case(font_folder_name)

        font_path = os.path.join(self.fonts_path, font_folder_name)
        if os.path.exists(font_path):
            shutil.rmtree(font_path)

        license_folder_name = self.to_snake_case(font_folder_name)
        license_path = os.path.join(self.licenses_path, license_folder_name)
        if os.path.exists(license_path):
            shutil.rmtree(license_path)

        self.remove_font_from_list(font_folder_name)
        print(f'{GREEN}{font_name} removed with success!{RESET}\n\n')


    def remove_font_from_list(self, font_folder_name):
        with open(self.fonts_list_path, 'r') as f:
            lines = f.readlines()

        pattern = re.compile(re.escape(font_folder_name), re.IGNORECASE)
        new_lines = [
            line for line in lines if not pattern.search(line)
        ]

        with open(self.fonts_list_path, 'w') as f:
            f.writelines(new_lines)

    def install_fonts(self):
        self.install_font()
        self.run()


    def uninstall_fonts(self):
        installed = []
        i = 0
        for font in os.listdir(self.fonts_path):
            i += 1
            installed.append(font)
            print(f'{i}. {font}')

        action = int(input('Type the number of the font to be removed: '))

        if (action >= 0 and action <= len(installed)):
            self.uninstall_font(installed[int(action) - 1])
        else:
            print('{RED}invalid input!{RESET}')
        action = input('uninnstall another font?')

        if action.lower() == 'y':
            self.uninstall_fonts()
        else:
            self.run()


    def run(self):
        print('-' * 50)
        print('FONTS INSTALLER')
        print('-' * 50)

        while (True):
            action = input('[I]nstall fonts\n[U]ninstall font\n[E]xit: ')

            if action.lower() == 'u':
                self.uninstall_fonts()
            elif action.lower() == 'i':
                self.install_fonts()
            else:
                break



if __name__ == '__main__':
    FontInstaller().run()
