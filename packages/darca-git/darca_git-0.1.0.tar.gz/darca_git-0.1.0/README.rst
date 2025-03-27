====================
Darca Git
====================

**Darca Git** is a lightweight abstraction over Git CLI commands, built to integrate with `darca-executor` and the Darca ecosystem.

|Build Status| |Deploy Status| |CodeCov| |Formatting| |License| |PyPi Version| |Docs|

.. |Build Status| image:: https://github.com/roelkist/darca-git/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/roelkist/darca-git/actions
.. |Deploy Status| image:: https://github.com/roelkist/darca-git/actions/workflows/cd.yml/badge.svg
   :target: https://github.com/roelkist/darca-git/actions
.. |Codecov| image:: https://codecov.io/gh/roelkist/darca-git/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/roelkist/darca-git
   :alt: Codecov
.. |Formatting| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black code style
.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
.. |PyPi Version| image:: https://img.shields.io/pypi/v/darca-git
   :target: https://pypi.org/project/darca-git/
   :alt: PyPi
.. |Docs| image:: https://img.shields.io/github/deployments/roelkist/darca-git/github-pages
   :target: https://roelkist.github.io/darca-git/
   :alt: GitHub Pages

- 🔐 Runs shell-safe commands via `darca-executor`
- 🧪 100% tested with `pytest`
- 🧰 Integrated with darca-space-git for space-aware Git

Installation
============

Clone and install the project using:

.. code-block:: bash

    make install

Usage
=====

.. code-block:: python

    from darca_git.git import Git

    git = Git()
    git.init("/your/repo")
    git.status("/your/repo")

Testing
=======

Run tests with full coverage:

.. code-block:: bash

    make test

Documentation
=============

Docs are built with Sphinx:

.. code-block:: bash

    make docs

Pre-commit Hooks
================

Check formatting, linting and more with:

.. code-block:: bash

    make precommit

Full quality check:

.. code-block:: bash

    make check
