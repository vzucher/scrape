import os
import subprocess

def extract_imports(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    imports = set()
    for line in lines:
        line = line.strip()
        if line.startswith('import ') or line.startswith('from '):
            imports.add(line.split()[1].split('.')[0])
    return imports

all_imports = set()
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            all_imports.update(extract_imports(os.path.join(root, file)))

print(all_imports)

# Get a list of installed packages and their versions
installed_packages = subprocess.getoutput('pip freeze')

# Filter the list
requirements = []
for package in installed_packages.split('\n'):
    name = package.split('==')[0].lower()
    for imp in all_imports:
        if imp in name:
            requirements.append(package)

# Write to requirements.txt
with open('requirements.txt', 'w') as f:
    for req in requirements:
        f.write(req + '\n')
