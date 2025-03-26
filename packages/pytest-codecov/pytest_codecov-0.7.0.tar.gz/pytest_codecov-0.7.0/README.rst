==============
pytest-codecov
==============

.. image:: https://img.shields.io/pypi/v/pytest-codecov.svg
    :target: https://pypi.org/project/pytest-codecov
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-codecov.svg
    :target: https://pypi.org/project/pytest-codecov
    :alt: Python versions

.. image:: https://github.com/seantis/pytest-codecov/actions/workflows/python-tox.yaml/badge.svg
    :target: https://github.com/seantis/pytest-codecov/actions
    :alt: Tests

.. image:: https://codecov.io/gh/seantis/pytest-codecov/branch/master/graph/badge.svg?token=CwujQmq61X
    :target: https://codecov.io/gh/seantis/pytest-codecov
    :alt: Codecov.io

Pytest plugin for uploading `pytest-cov`_ results to `codecov.io`_

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Features
--------

* Uploads coverage results to `codecov.io` at the end of the tests.
* Detects current project slug, branch and commit using `GitPython`, when installed and running inside a git repository.


Requirements
------------

* `pytest-cov`_
* `requests`_
* `GitPython`_ (Optional, for auto detecting some meta data)


Installation
------------

You can install "pytest-codecov" via `pip`_ from `PyPI`_::

    $ pip install pytest-codecov


Usage
-----

* Add :code:`--codecov` to pytest arguments to enable upload
* Supply your Codecov token either through :code:`--codecov-token=` or `CODECOV_TOKEN` environment variable. Refer to your CI's documentation to properly secure that token.


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.


License
-------

Distributed under the terms of the `MIT`_ license, "pytest-codecov" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/seantis/pytest-codecov/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
.. _`pytest-cov`: https://github.com/pytest-dev/pytest-cov
.. _`codecov.io`: https://codecov.io
.. _`requests`: https://github.com/psf/requests
.. _`GitPython`: https://github.com/gitpython-developers/GitPython
