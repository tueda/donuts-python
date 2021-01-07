Donuts-Python
=============

Python binding to the `Donuts`_ wrapper for `Rings`_.


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
    >>> Polynomial('2*x^2 - 2*x^3 + 2*x^2*y - 2*x^3*y').factors
    (Polynomial('-2'), Polynomial('x'), Polynomial('x'), Polynomial('-1+x'), Polynomial('1+y'))


Development
-----------

.. The code is tested by "readme_dev" in .gitlab-ci.yml and .github/workflows/ci.yml.

.. code:: shell

    poetry install
    poetry run pre-commit install
    poetry run pre-commit install --hook-type commit-msg

    git submodule update --init
    poetry run invoke build

    poetry run invoke fmt
    poetry run invoke lint
    poetry run invoke test
    poetry run invoke bench
    poetry run invoke doc

    DONUTS_PYTHON_BACKEND=pyjnius poetry run invoke test
    DONUTS_PYTHON_BACKEND=py4j    poetry run invoke test

    poetry run pip install wheel
    poetry run invoke build --sdist --wheel


License
-------

Donuts-Python is distributed under the MIT license.

The wheel contains a fat JAR file generated from the following dependencies:

* `Donuts`_ (MIT)
* `Rings`_ (Apache 2.0)
* `libdivide4j`_ (Apache 2.0)
* `Combinatorics for Java`_ (Apache 2.0)
* `Apache Commons Math`_ (Apache 2.0)
* `GNU Trove`_ (LGPL 2.1)


.. _Donuts: https://github.com/tueda/donuts
.. _Rings:  https://github.com/PoslavskySV/rings
.. _libdivide4j: https://github.com/PoslavskySV/libdivide4j
.. _Combinatorics for Java: https://github.com/PoslavskySV/combinatorics
.. _Apache Commons Math: https://github.com/apache/commons-math
.. _GNU Trove: https://bitbucket.org/trove4j/trove
