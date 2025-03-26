from setuptools import setup

name = "types-shapely"
description = "Typing stubs for shapely"
long_description = '''
## Typing stubs for shapely

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`shapely`](https://github.com/shapely/shapely) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `shapely`. This version of
`types-shapely` aims to provide accurate annotations for
`shapely==2.0.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/shapely`](https://github.com/python/typeshed/tree/main/stubs/shapely)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.397,
and pytype 2024.10.11.
It was generated from typeshed commit
[`4fff7b7d0165120bf79928534c88dffffdcb5da2`](https://github.com/python/typeshed/commit/4fff7b7d0165120bf79928534c88dffffdcb5da2).
'''.lstrip()

setup(name=name,
      version="2.0.0.20250326",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/shapely.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['numpy>=1.20'],
      packages=['shapely-stubs'],
      package_data={'shapely-stubs': ['__init__.pyi', '_enum.pyi', '_geometry.pyi', '_ragged_array.pyi', '_typing.pyi', '_version.pyi', 'affinity.pyi', 'algorithms/__init__.pyi', 'algorithms/cga.pyi', 'algorithms/polylabel.pyi', 'constructive.pyi', 'coordinates.pyi', 'coords.pyi', 'creation.pyi', 'decorators.pyi', 'errors.pyi', 'geometry/__init__.pyi', 'geometry/base.pyi', 'geometry/collection.pyi', 'geometry/geo.pyi', 'geometry/linestring.pyi', 'geometry/multilinestring.pyi', 'geometry/multipoint.pyi', 'geometry/multipolygon.pyi', 'geometry/point.pyi', 'geometry/polygon.pyi', 'geos.pyi', 'io.pyi', 'lib.pyi', 'linear.pyi', 'measurement.pyi', 'ops.pyi', 'plotting.pyi', 'predicates.pyi', 'prepared.pyi', 'set_operations.pyi', 'speedups.pyi', 'strtree.pyi', 'testing.pyi', 'validation.pyi', 'vectorized/__init__.pyi', 'wkb.pyi', 'wkt.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
