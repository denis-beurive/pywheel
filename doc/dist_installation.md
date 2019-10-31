# Distribution installation

Let's assume that you want to install the source distribution into your local project.
We assume that the local project has a virtual environment. 

> `pip install --user pipenv`, `pipenv install --python 3`, `pipenv shell`.

We assume that the source distribution is located in the file "`/path/to/dist/my_hello_world-0.1.tar.gz`".

There are 2 installation modes:
* the standard mode.
* the editable/developer mode.

When a distribution is installed in standard mode, it is used as a dependency.
In this case the distribution is installed under `.virtualenvs` (or `venv`).

When a distribution is installed in editable/developer mode, it is installed so it can be modified by the developer.
In this case the distribution is not installed under `.virtualenvs` (or `venv`).

## Standard mode

### Nominal/standard installation

To install the distribution in _standard mode_, run the command below:

    pip install "/path/to/dist/my_hello_world-0.1.tar.gz"

or

    pipenv install "/path/to/dist/my_hello_world-0.1.tar.gz"

If you want to make sure that the distribution is installed, you can run one of the following command:

* `pipenv graph`
* `pip list` or  `pipenv run pip list`
* `pip show my_hello_world` or `pip show my_hello_world --files` or `pipenv run pip show my_hello_world`

If you want to know where the distribution files are installed, you can run the following command:

    python -c "import my_package.my_module; print(my_package.my_module.__file__)"

### Installation with extra feature enabled

The list of extra features that can be enabled are listed within the script `setup.py`.

For example:

    extras_require={
        "color": ["clint==0.5.1"]
    }

Let's assume that we want to activate the optional feature which consists in the colorization of the script's output:

	pip install --find-links=/path/to/sdist/my_hello_world-0.1.tar.gz  "my_hello_world [color]"

This command will install an additional dependency: `clint`.

> See [this link](https://packaging.python.org/tutorials/installing-packages/#installing-from-local-archives)

You can verify that the distribution is installed, along with the additional dependency:

    pip show clint
	python -c "import clint; import my_package.my_module; print(my_package.my_module.__file__)"

## Editable/developer mode

### Using pip

Installing the distribution in _editable/developer_ mode means that you install it so you can work on the distribution
source code. 

> See: [Editable Dependencies](https://pipenv-fork.readthedocs.io/en/latest/basics.html#editable-dependencies-e-g-e)

To install the distribution in _editable/developer_ mode:

* get the source code of the distribution (clone a GIT repository, expand an archive...).
* the run the following command: `pip install -e .` (please note that `pipenv install -e .` also works).

For example (we don't use any virtual environment), using `pip`:

    git clone https://github.com/denis-beurive/pywheel.git
    cd pywheel
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    pip install -e .
    python run_unittest.py
    
Please note that:

* you can include a _requirements file_ from within a _requirements file_.
* you can include pip command line options within a _requirements file_.

For example, you could modify the file [requirements-dev.txt](../requirements-dev.txt) this way:

    -r requirements.txt
    -e .
    xmlrunner==1.7.7

Thus, you just have to  run `pip install -r requirements-dev.txt`.
It will install the requirements listed in the file `requirements.txt` (`-r requirements.txt`) and it will install the
distribution in _editable/developer_ mode (`-e .`).
     
> See [Editable Dependencies](https://pipenv-fork.readthedocs.io/en/latest/basics.html#editable-dependencies-e-g-e).

Make sure that the module `my_package/my_module.py` is accessible through `PYTHONPATH`.

    python -c "import sys; print(\"\n\".join([f\"{f}\" for f in sys.path]))"

or:
    
    python -c "import my_package.my_module; print(my_package.my_module.__file__)"

You should see the path to the local directory `lib`.

### Using pipenv

The list of commands bellow will install the distribution in editable/developer mode (`-e .`), including the development
environment (`--dev`).

    git clone https://github.com/denis-beurive/pywheel.git
    cd pywheel
    pipenv install -e . --dev
    
Please note that the option `--dev` will make use of the section `[dev-packages]` of the file `Pipfile`.
This section has been used to generate the requirements file `requirements-dev.txt`
(`pipenv lock --requirements --dev > requirements-dev.txt`).

Make sure that the environment variable `PYTHONPATH` is well configured:

    pipenv shell
    pipenv --venv
    python -c "import sys; print('\n'.join([f'{p}' for p in sys.path]))"
    python -c "import my_package.my_module; print(my_package.my_module.__file__)"
