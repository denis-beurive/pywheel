# Generating the wheel

Install `wheel` and `setuptools`, and update the environment:

    pipenv install wheel
    pipenv install setuptools
    pipenv update

Then create the wheel:

    python setup.py sdist bdist_wheel

* `sdist`: a _source distribution_. It contains everything you need to _recompile_ the distribution.
  It will be created into the directory `dist`.
* `bdist_wheel`: a _built distribution_. It creates a _compiled distribution_ (`*.pyc`, `*.so`, `*.dll`...).
  The result is an archive that is specific to a platform (for example _linux-x86_64_) and to a version of Python, and
  that can be installed simply by extracting it into the root of your filesystem.
  It will be created into the directory `build`.

> To get the full list of available distribution types, run this command: `python setup.py --help-commands`.
