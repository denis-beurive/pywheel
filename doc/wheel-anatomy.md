# Anatomy of a wheel

See [this documentation](https://setuptools.readthedocs.io/en/latest/setuptools.html#basic-use).

See [this example](../setup.py).

# Notes

## Implicit Namespace Packages
 
Since Python 3.3 the presence of the file `__init__.py` in the package directory is not mandatory anymore.
See "_Implicit Namespace Packages_" at [https://www.python.org/dev/peps/pep-0420/](https://www.python.org/dev/peps/pep-0420/).

However, for `setuptools.find_packages()` to work, the package directories must include a file named "__init__.py".
See: [https://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages](https://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages).

If you use [implicit namespace packages](https://www.python.org/dev/peps/pep-0420/) (since Python 3.3), then you must
use the method `setuptools.find_namespace_packages()`.
See [https://setuptools.readthedocs.io/en/latest/setuptools.html#find-namespace-packages](https://setuptools.readthedocs.io/en/latest/setuptools.html#find-namespace-packages).

## package_dir vs packages

* `packages` lists **the names** of all the packages.
* `package_dir` specifies **the paths of the directories** that contain the packages (listed by the key `packages`).

> See [Listing whole packages](https://docs.python.org/3.6/distutils/setupscript.html#listing-whole-packages).

## The data files

The key `data_files` specifies the paths to the "extra files" that must be included into the distribution.

Please keep in mind that the script `setup.py` will be executed during the installation process.
This script may need some files in order to proceed to the installation of the distribution.
For example, [this setup script](../setup.py) needs the following files: `requirements.txt`,
`requirements-dev.txt` and `data/description.md`. Therefore, these files must be included within the distribution
archive. 

See [Installing Additional Files](https://docs.python.org/3.6/distutils/setupscript.html#installing-additional-files).

Example:

    data_files=[('target', ['data/description.md'])]
    
* the first element of the tuple represents the target directory (within the distribution archive).
* the second element of the tuple represents the path to the file that must be copied into the target directory.

This line means that the file `data/description.md` will be copied into the target directory `target` (within the
distribution archive).

Please note that in the example "`setup.py`" file, we have:

    long_description_path = os.path.join(__DIR__, 'data', 'description.md')
    
    setuptools.setup(
        ...
        data_files=[('data', ['data/description.md'])]
    )

When the script "`setup.py`" will be run to install the distribution, it will look for the file which path is
`os.path.join(__DIR__, 'data', 'description.md')`. Thus the file "`data/description.md`" must be included into the
distribution archive (as a data file).

## "entry points" vs "scripts"

* The [entry points](https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html#the-console-scripts-entry-point).
* The [scripts](https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html#the-scripts-keyword-argument).


    setuptools.setup(
        ...
        scripts=['bin/hello_world.py'],
        entry_points={
            'console_scripts': [
                'hello = my_package.my_module:main',
            ]
        }
    )

Declaring a **script** only tells the package installer that it must replace the path to the interpreter that appears after
the `#!` by the path to the current interpreter.

Declaring an entry point will create an executable which path will be added to the environment variable `PATH`.
In the example above, the executable will be `hello.exe` (under Windows).
And this executable will execute the function `main` from the module `my_package.my_module`.

## "install_requires" vs "extras_require"

* `install_requires` lists all the distribution dependencies for _nominal/standard_ installation.
* `extras_require`: this parameter lists _additional_ dependencies for installations that include _optional/extra_
  features. Please note that we are talking about _additional_ dependencies here: the dependencies for the
  _nominal/standard_ installation will be installed. 

To specify that we want to run the installation process for an extra feature, we just declare this feature after the
name of the package, between brackets. For example: "`my_hello_world [color]`"

    pip install --find-links=/path/to/sdist/my_hello_world-0.1.tar.gz "my_hello_world [color]"
