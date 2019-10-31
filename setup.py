# See: https://setuptools.readthedocs.io/en/latest/setuptools.html
#
# Note: please keep in mind that this script will be executed within 2 environments:
#          1. the "source environment": the environment where the distribution is generated.
#             Typically: python setup.py sdist
#          2. the "installation environment": the environment where the distribution is installed.
#             Typically: pip install /path/to/sdist/my_hello_world-0.1.tar.gz
#             In this environment, the files that are needed for the installation will be searched
#             within the distribution archive (that is: /path/to/sdist/my_hello_world-0.1.tar.gz).

import setuptools
from typing import List
import os
import re
import sys


# See: https://docs.python.org/3.6/distutils/setupscript.html
# WARNING: make sure to declare the file "data/description.md" as a "data file" (see key
#          "data_files").
__DIR__ = os.path.dirname(os.path.abspath(__file__))
long_description_path = os.path.join(__DIR__, 'data', 'description.md')

with open(long_description_path, "r") as fh:
    long_description = fh.read()

# Get the list of packages under the directory "lib".
#
# Please note that, since Python 3.3 the presence of the file "__init__.py" in the package
# directory is not mandatory anymore. See "Implicit Namespace Packages" at
# https://www.python.org/dev/peps/pep-0420/
#
# However, for "setuptools.find_packages()" to work, you must create a file called "__init__.py"
# in the package directory.
#
# See: https://setuptools.readthedocs.io/en/latest/setuptools.html
#
# If you use implicit namespace packages (since Python 3.3), then you can use the method
# "setuptools.find_namespace_packages()".

use_implicit_namespace_packages = False

lib_dir = os.path.join(__DIR__, 'lib')
if use_implicit_namespace_packages:
    # No package initializer "__init__.py" is required (since Python 3.3).
    packages_lib = setuptools.find_namespace_packages(where=lib_dir)
else:
    # Package initializers "__init__.py" are required.
    packages_lib = setuptools.find_packages(where=lib_dir)

print('Packages under "lib":\n' + '\n'.join([f'\t* {p}' for p in packages_lib]) + "\n\n")
print(f'Installation prefix: "{sys.prefix}".' + "\n\n")

# Load the requirements.
#
# Please note that the requirement files must be generated prior to this operation:
#
#    * pipenv lock --requirements > requirements.txt
#    * pipenv lock --requirements --dev > requirements-dev.txt
#
# See the sections "[dev-packages]" and "[packages]" of the "Pipfile".

def load_requirements(name: str) -> List[str]:
    """Load a given requirement file and generate the corresponding data
    structure that represents the requirements.

    :param name: name of the requirement file to load.
    :return: the corresponding data structure that represents the requirements.
    """
    dependencies: List[str] = []
    dep_matcher = re.compile('^[^=<>\\s]+\\s*[=<>]+\\s*[^=<>\\s]+$')
    with open(name, 'r') as fd:
        for line in fd.read().split("\n"):
            line.strip()
            if dep_matcher.match(line):
                dependencies.append(line)
    return dependencies


nominal_requirements = load_requirements('requirements.txt')
tests_requirements = load_requirements('requirements-dev.txt')

setuptools.setup(
    author="Me",
    author_email="me@example.com",
    # The key "packages" lists the *names* of the packages. It does not list the package
    # directories. The paths to the directories are defined by the key "package_dir".
    packages=packages_lib,
    # See https://docs.python.org/3.6/distutils/setupscript.html#listing-whole-packages
    # Here, we say that all the package directories are located in the directory "src". It is
    # possible to assign specific directories for specific packages.
    package_dir={'': 'lib'},
    # **WARNING**: do NOT use the name "hello_world" !!!
    # A package with the same name already exists !!!
    name="my_hello_world",
    version="0.1",
    description="Say hello to the World.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # See: https://docs.python.org/3.6/distutils/setupscript.html#installing-scripts
    # This key simply tells the installer that it must replace the path to the interpreter after
    # the "#!" (if present) by the path to the current interpreter (or the one passed through the
    # command line), in the specified list of files.
    scripts=['bin/hello_world.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    # See: https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
    # Once the package is installed, the console script "hello" will be available. To see the list
    # of all entry points for a given package you can use the command bellow:
    #
    #    pip show hello_world
    entry_points={
        'console_scripts': [
            'hello = my_package.my_module:main'
        ]
    },
    # Data files: files that must be included into the archive that is the wheel.
    #
    # See: https://docs.python.org/3.6/distutils/setupscript.html#installing-additional-files
    #
    # Make sure to add all files used by the script "setup.py". In this case:
    # - requirements.txt
    # - requirements-dev.txt
    # - data/description.md
    #
    # "data_files" is an array of tuples. Each tuple contains 2 elements.
    # - The first element of the tuple (ex: "data") represents the target directory.
    # - The second element of the tuple (ex: "data/description.md") represents the file that will
    #   be copied into the distribution.
    data_files=[('', ['requirements.txt', 'requirements-dev.txt']),
                ('data', ['data/description.md'])],
    # List the requirements for the nominal/standard use of the distribution.
    # Related command:
    #
    #    pip install /path/to/dist/my_hello_world-0.1.tar.gz
    install_requires=nominal_requirements,
    # List the requirements needed for optional features.
    # Related command:
    #
    #    pip install --find-links=/path/to/sdist/my_hello_world-0.1.tar.gz "my_hello_world [color]"
    extras_require={
        "color": ["clint==0.5.1"]
    },
    # List the requirements for the execution of the tests.
    # Related command:
    #
    #    python setup.py test
    #
    # Please note that the command "test" is deprecated! Thus, you should not use the parameter
    # "tests_require".
    tests_require=tests_requirements
)
