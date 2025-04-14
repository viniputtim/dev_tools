import re
import os


def to_natural_case(name):
    name = re.sub(r'[_\-]+', ' ', name)
    name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)

    return name.lower().strip()


def extract(text, name):
    content = re.split(r"(?m)^[-_]{3,}$", text)[0]
    return f'*{name}*\n\n{content.strip()}\n\n'


credits = ''
folder = '/home/viniciuspm/Desenvolvimento/its_about_cards/docs/LICENSES'

for root, dirs, files in os.walk(folder):
        for file in files:
            with open(os.path.join(folder, root, file), 'r') as f:
                text = f.read()
                file_name = os.path.basename(root)
                file_name = to_natural_case(file_name)
                credits += extract(text, file_name)

print(credits)
