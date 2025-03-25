#!/usr/bin/env python3
import os
import sys
import ast
import argparse
import pkgutil
import importlib.metadata
import requests
from pathlib import Path

# Get list of standard library modules
std_lib_modules = set(m[1] for m in pkgutil.iter_modules())
# Add other standard modules that might not be caught
std_lib_modules.update(['os', 'sys', 'time', 're', 'math', 'random', 'datetime', 'json',
                        'collections', 'itertools', 'functools', 'typing', 'pathlib'])

class ImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = set()
        
    def visit_Import(self, node):
        for name in node.names:
            self.imports.add(name.name.split('.')[0])
        self.generic_visit(node)
        
    def visit_ImportFrom(self, node):
        if node.module and node.level == 0:  # Ignore relative imports
            self.imports.add(node.module.split('.')[0])
        self.generic_visit(node)

def scan_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            tree = ast.parse(file.read())
            visitor = ImportVisitor()
            visitor.visit(tree)
            return visitor.imports
        except SyntaxError:
            print(f"Syntax error in {file_path}, skipping...")
            return set()

def is_third_party(module_name):
    return module_name not in std_lib_modules

def get_installed_version(package):
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return None

def get_latest_version(package):
    try:
        response = requests.get(f"https://pypi.org/pypi/{package}/json", timeout=5)
        if response.status_code == 200:
            return response.json()['info']['version']
        return None
    except Exception as e:
        print(f"Error fetching version for {package}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Generate requirements.txt by scanning Python imports')
    parser.add_argument('--dir', '-d', default='.', help='Project directory to scan (default: current directory)')
    parser.add_argument('--output', '-o', default='requirements.txt', help='Output file (default: requirements.txt)')
    parser.add_argument('--installed', '-i', action='store_true', help='Use installed versions instead of latest')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    project_dir = Path(args.dir)
    if not project_dir.exists() or not project_dir.is_dir():
        print(f"Error: {args.dir} is not a valid directory")
        sys.exit(1)
    
    print(f"Scanning Python files in {project_dir.absolute()}...")
    
    all_imports = set()
    python_files = list(project_dir.glob('**/*.py'))
    
    if not python_files:
        print("No Python files found!")
        sys.exit(1)
    
    for file_path in python_files:
        if args.verbose:
            print(f"Scanning {file_path}...")
        imports = scan_file(file_path)
        all_imports.update(imports)
    
    third_party_imports = {module for module in all_imports if is_third_party(module)}
    
    if not third_party_imports:
        print("No third-party imports found!")
        sys.exit(0)
    
    print(f"Found {len(third_party_imports)} third-party packages")
    
    requirements = {}
    for package in sorted(third_party_imports):
        if args.installed:
            version = get_installed_version(package)
            if version:
                requirements[package] = version
                if args.verbose:
                    print(f"Found installed package: {package}=={version}")
            else:
                print(f"Warning: {package} is imported but not installed")
        else:
            version = get_latest_version(package)
            if version:
                requirements[package] = version
                if args.verbose:
                    print(f"Found latest version for {package}: {version}")
            else:
                print(f"Warning: Could not find {package} on PyPI")
    
    if not requirements:
        print("No requirements could be determined!")
        sys.exit(1)
    
    with open(args.output, 'w') as f:
        for package, version in requirements.items():
            f.write(f"{package}=={version}\n")
    
    print(f"Successfully generated {args.output} with {len(requirements)} packages")

if __name__ == "__main__":
    main()