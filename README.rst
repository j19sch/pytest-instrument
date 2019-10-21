=================
pytest-instrument
=================

.. image:: https://img.shields.io/pypi/v/pytest-instrument.svg
    :target: https://pypi.org/project/pytest-instrument
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-instrument.svg
    :target: https://pypi.org/project/pytest-instrument
    :alt: Python versions

.. image:: https://circleci.com/gh/j19sch/pytest-instrument/tree/master.svg?style=svg
    :target: https://circleci.com/gh/j19sch/pytest-instrument/tree/master
    :alt: See Build Status on Circle CI

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
    :target: https://github.com/j19sch/pytest-logfest/blob/master/LICENSE
    :alt: MIT license

pytest plugin to instrument tests

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Features
--------

* TODO


Labels and tags
~~~~~~~~~~~~~~~
You can add labels and tags with `@pytest.mark.instrument()`. `args` become labels; `kwargs` become tags.

There are also two hook functions to manipulate labels and tags after they have been set:

- `pytest_instrument_labels`
- `pytest_instrument_tags`

Fixtures
~~~~~~~~
In case you want to filter out a fixture, e.g. because every test uses it by default, you can use the
`pytest_instrument_fixtures()` hook function.


Requirements
------------

* TODO


Installation
------------

You can't yet install "pytest-instrument" via `pip`_ from `PyPI`_::

    $ pip install pytest-instrument


Usage
-----

* TODO

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-instrument" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/j19sch/pytest-instrument/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
