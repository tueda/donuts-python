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


Example
-------

.. code:: python

    >>> from donuts import *
    >>> a = Polynomial('1 + x + y')
    >>> b = Polynomial('1 + y + z')
    >>> g = a + b
    >>> g
    Polynomial('2+z+2*y+x')
    >>> ag = a * g
    >>> bg = b * g
    >>> ag.gcd(bg)  # must be equal to g
    Polynomial('2+z+2*y+x')
    >>> ag / bg  # same as RationalFunction(ag, bg)
    RationalFunction('(1+y+x)/(1+z+y)')
    >>> Polynomial('-2*x^4*y^3 + 2*x^3*y^4 + 2*x^2*y^5 - 2*x*y^6').factorize()
    [Polynomial('-2*x*y^2'), Polynomial('-1*y+x'), Polynomial('-1*y+x'), Polynomial('y+x')]


Development
-----------

.. code:: shell

    git clone --recursive https://github.com/tueda/donuts-python
    cd donuts-python
    pipenv install --dev
    pipenv run python setup.py build

    # Run predefined scripts.
    pipenv run fmt
    pipenv run lint
    pipenv run test
    pipenv run bench
    pipenv run doc

    # Or run indivisual commands in a virtualenv.
    pipenv shell
    black .
    isort -y
    flake8
    mypy .
    pytest --benchmark-disable --cov=donuts
    pytest --benchmark-only
    make -C docs html

    # Git hooks.
    pre-commit install
    pre-commit install --hook-type commit-msg


License
-------

MIT
