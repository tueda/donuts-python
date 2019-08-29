Donuts-Python
=============

Python binding to the `Donuts`_ wrapper for `Rings`_.

.. _Donuts: https://github.com/tueda/donuts
.. _Rings:  https://github.com/PoslavskySV/rings


Requirements
------------

* Python 3.7 or later
* JDK 8 or later


Installation
------------

.. code:: shell

    pip install git+https://github.com/tueda/donuts-python


For developers
--------------

.. code:: shell

    git clone --recursive https://github.com/tueda/donuts-python
    cd donuts-python
    pipenv install --dev
    pipenv run python setup.py build

    # Run predefined scripts.
    pipenv run fmt
    pipenv run lint
    pipenv run test

    # Or run indivisual commands in a virtualenv.
    pipenv shell
    black .
    isort -y
    flake8
    mypy .
    pytest --cov=donuts
