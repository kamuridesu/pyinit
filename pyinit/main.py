import os
import sys
from pprint import pprint
from pathlib import Path
from venv import create

setup_template = """[metadata]
name={name}
version={version}
description={description}
author={author}
author_email={email}
url={repository}
keywords={keywords}
license={license}
[options]
zip_safe = False
packages =
    {name}
"""


main_template = """import {name}


def main():
    ...


if __name__ == \"__main__\":
    main()
"""


def create_dir(dir_name: str):
    if not os.path.isdir(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError:
            print("Failed to create dir!")
            exit(1)


def argparse():
    base_path = Path(".").parent.absolute()
    yes = False
    venv = False
    args = sys.argv[1:]
    if "-y" in args:
        yes = True
        args.pop(args.index("-y"))
    if "--venv" in args:
        venv = True
        args.pop(args.index("--venv"))
    if len(args) > 1:
        print("Error! Can only create one project per execution!")
        exit(1)
    if len(args) == 1:
        base_path = args[0]
    project_data = {
        "name": os.path.basename(base_path),
        "version": "0.1.0",
        "description": "",
        "author": "",
        "email": "",
        "repository": "",
        "keywords": "python",
        "license": "",
    }
    if not yes:
        for k in project_data.copy():
            data = input(f"{k.capitalize()}: ")
            if data:
                project_data[k] = data
    generate_files(base_path, venv, project_data)


def generate_files(base_path, venv, project_data):
    pprint(project_data)
    project_path = os.path.join(base_path, project_data['name'])
    if not os.path.isdir(project_path):
        create_dir(project_path)
    if venv:
        create(os.path.join(base_path, "venv"), with_pip=True)
    create_dir(os.path.join(project_path, "src"))
    with open(os.path.join(project_path, "src", "__init__.py"), "w") as f:
        f.write("")
    if not os.path.exists(main_path := os.path.join(base_path, "main.py")):
        with open(main_path, "w") as f:
            f.write(main_template.format(name=project_data['name']))
    with open(os.path.join(base_path, "setup.cfg"), "w") as f:
        f.write(setup_template.format(**project_data))
    with open(os.path.join(base_path, "pyproject.toml"), 'w') as f:
        f.write("""[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta\"""")


def main():
    argparse()


if __name__ == "__main__":
    main()
