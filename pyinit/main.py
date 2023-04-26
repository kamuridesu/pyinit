import os
import sys
from pprint import pprint
from pathlib import Path
from venv import create


def generate_gitignore(path: str):
    content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/#use-with-ide
.pdm.toml

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/
"""
    with open(os.path.join(path, ".gitignore"), "w") as f:
        f.write(content)


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
        for k, v in project_data.copy().items():
            data = input(f"{k.capitalize()} ({v}): ")
            if data:
                project_data[k] = data
    generate_files(base_path, venv, project_data)


def generate_files(base_path, venv, project_data):
    pprint(project_data)
    project_path = os.path.join(base_path, project_data["name"])
    if not os.path.isdir(project_path):
        create_dir(project_path)
    if venv:
        print("Creating virtualenv, this may take a while depending on your system")
        create(os.path.join(base_path, "venv"), with_pip=True)
    create_dir(os.path.join(project_path, "src"))
    with open(os.path.join(project_path, "src", "__init__.py"), "w") as f:
        f.write("")
    if not os.path.exists(main_path := os.path.join(base_path, "main.py")):
        with open(main_path, "w") as f:
            f.write(main_template.format(name=project_data["name"]))
    with open(os.path.join(base_path, "setup.cfg"), "w") as f:
        f.write(setup_template.format(**project_data))
    with open(os.path.join(base_path, "pyproject.toml"), "w") as f:
        f.write(
            """[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta\""""
        )
    generate_gitignore(base_path)


def main():
    argparse()


if __name__ == "__main__":
    main()
