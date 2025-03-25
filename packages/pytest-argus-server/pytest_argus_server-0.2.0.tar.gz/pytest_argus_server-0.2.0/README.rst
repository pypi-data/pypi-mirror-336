===================
pytest-argus-server
===================

.. image:: https://img.shields.io/pypi/v/pytest-argus-server.svg
    :target: https://pypi.org/project/pytest-argus-server
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-argus-server.svg
    :target: https://pypi.org/project/pytest-argus-server
    :alt: Python versions

.. image:: https://github.com/Uninett/pytest-argus-server/actions/workflows/main.yml/badge.svg
    :target: https://github.com/Uninett/pytest-argus-server/actions/workflows/main.yml
    :alt: See Build Status on GitHub Actions

A `pytest`_ plugin that provides a running `Argus`_ API server for tests.

----

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Features
--------

* Fixtures that will provide tests with a running Argus API server (using Docker Compose)

Requirements
------------

* `Docker Compose`_

Installation
------------

You can install "pytest-argus-server" via `pip`_ from `PyPI`_::

    $ pip install pytest-argus-server


Usage
-----

Installing this package will automatically make it available in `pytest`_.

Extra pytest command line arguments
+++++++++++++++++++++++++++++++++++

By default, this plugin will run the *latest available* Argus server Docker
image.  The actually deployed version can be controlled by adding the
``--argus-version`` command line option to pytest::

  pytest --argus-version=1.30.0 tests/

Provided fixtures
+++++++++++++++++

The main fixtures provided by this plugin are the session-scoped
``argus_api_url`` and ``argus_source_system_token``.

``argus_api_url``
~~~~~~~~~~~~~~~~~

When used by a test, this will ensure an Argus server is running and ready to
take requests.  It returns the base URL of the running API:

.. code-block:: python

    def test_url_should_be_as_expected(argus_api_url):
        assert argus_api_url == "http://localhost:8000/api/v2/"


``argus_source_system_token``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This token will create a test source system and return a valid API token for
accessing the API as this test source.

.. code-block:: python

    def test_fetch_incidents(argus_api_url, argus_source_system_token):
        assert requests.get(
            f"{argus_api_url}/incidents/",
            headers={"Authorization": f"Token {argus_source_system_token}"}
        ).status_code == 200


Bugs
----

* The port number of the launched API server is hard-coded to `8000`.

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `Apache Software License 2.0`_ license, "pytest-argus-server" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Argus`: https://github.com/Uninett/argus
.. _`Docker Compose`: https://docs.docker.com/compose/
.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: https://opensource.org/licenses/MIT
.. _`BSD-3`: https://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: https://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: https://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/Uninett/pytest-argus-server/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
