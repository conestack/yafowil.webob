Changes
=======

2.0.1 (unreleased)
------------------

- Fix ``WebObRequestAdapter.__iter__`` returning ``None`` instead of an
  empty iterator for an unset request, ``iter(adapter)`` raised ``TypeError``.
  [rnix]

- Modernise the code ruff flags as outdated: ``class X(object)``. Behaviour
  unchanged.
  [rnix]

- Sort the imports with ruff (one per line, ``from`` imports first, no
  sections) and format the code with ``ruff format`` (90 characters per line,
  single quotes).
  [rnix]

- Add ``qa.ruff`` domain to Makefile and pin the ruff configuration in
  ``pyproject.toml``, ``make check`` runs ``ruff check``.
  [rnix]

- Add tests, the package had none. Add ``test`` extra and fix
  ``mxmake-source-path`` in ``mx.ini``.
  [rnix]

- Drop the Python 2 remnants: ``yafowil.compat`` usage, ``IS_PY2`` branches and
  the ``collections`` import fallback.
  [rnix]


2.0.0 (2026-02-03)
------------------

- Refactor package layout to use ``pyproject.toml`` and implicit namespace packages.
  [rnix]


1.5 (2025-10-28)
----------------

- Pin upper versions of dependencies.
  [rnix]


1.4 (2022-12-05)
----------------

- Release wheel.
  [rnix]

- Python 3.10 support.
  [rnix]


1.3 (2018-07-16)
----------------

- Python 3 support.
  [rnix]


1.2
---

- Use ``yafowil.utils.entry_point`` decorator.
  [rnix]


1.1.2
-----

- Docs
  [jensens]


1.1.1
-----

- Provide translate callable for pyramid. soft dependency
  [rnix, 2012-04-24]


1.1
---

- use entry point for registration of webob preprocessor. depend on YAFOWIL 1.3
  [jensens, 2012-03-19]


1.0
---

- made it work
  [jensens, rnix, et al, 2010-12-27]
