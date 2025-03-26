from setuptools import setup

name = "types-jwcrypto"
description = "Typing stubs for jwcrypto"
long_description = '''
## Typing stubs for jwcrypto

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`jwcrypto`](https://github.com/latchset/jwcrypto) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `jwcrypto`. This version of
`types-jwcrypto` aims to provide accurate annotations for
`jwcrypto==1.5.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/jwcrypto`](https://github.com/python/typeshed/tree/main/stubs/jwcrypto)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.397,
and pytype 2024.10.11.
It was generated from typeshed commit
[`4fff7b7d0165120bf79928534c88dffffdcb5da2`](https://github.com/python/typeshed/commit/4fff7b7d0165120bf79928534c88dffffdcb5da2).
'''.lstrip()

setup(name=name,
      version="1.5.0.20250326",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/jwcrypto.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['cryptography'],
      packages=['jwcrypto-stubs'],
      package_data={'jwcrypto-stubs': ['__init__.pyi', 'common.pyi', 'jwa.pyi', 'jwe.pyi', 'jwk.pyi', 'jws.pyi', 'jwt.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
