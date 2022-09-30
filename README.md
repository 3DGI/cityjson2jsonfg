# CityJSON to JSON-FG

*A command line tool for converting CityJSON files to JSON-FG format.*

*JSON-FG* stands for [*OGC Features and Geometries JSON*](https://github.com/opengeospatial/ogc-feat-geo-json), which is (currently) a candidate standard.
JSON-FG extends GeoJSON to support a wider range of use cases.
For *cityjson2jsonfg* the most important capability of JSON-FG is 3D data storage, since [CityJSON](https://www.cityjson.org/) is a 3D spatial data format.
CityJSON is a JSON-based encoding for storing 3D city models, also called digital maquettes or digital twins.

Supported versions:

- CityJSON: 1.1
- JSON-FG: 0.1

## Installation

Required python: >= 3.8

Additionally, you need a relatively new version of `pip` and `setuptools` that supports building from `pyproject.toml` files.

You can install *cityjson2jsonfg* with pip.

```shell
pip install cityjson2jsonfg
```

## Usage

Convert a single CityJSON file to JSON-FG.

```shell
cityjson2jsonfg <input.city.json> <output.fg.json>
```

See the help menu and the tool version

```shell
cityjson2jsonfg --help
cityjson2jsonfg --version
```

### Pipe from cjio

[cjio]() is a CLI tool for manipulating 3D city models that are stored in CityJSON files.
You can pipe cjio's output directly into *cityjson2jsonfg* without saving an intermedate file.
This is particularly useful if you want to modify the citymodel before the conversion.
For instance, upgrade the CityJSON file to v1.1 and then convert it to JSON-FG.

```shell
cjio --suppress_msg <input.city.json> upgrade save stdout | cityjson2jsonfg - <output.fg.json>
```

## Limitations

Version 1.0 was primarily developed to convert CityJSON files of the Dutch [3D BAG](https://3dbag.nl/en/viewer) and [3D Basisvoorziening](https://www.pdok.nl/introductie/-/article/3d-basisvoorziening-1) data sets.
Conversion from other data sets might not work.

## Converted data

A subset of the 3D BAG and 3D Basisvoorziening is available at [https://data.3dgi.xyz/jsonfg](https://data.3dgi.xyz/jsonfg).
Both the source and converted files are provided.

## CityJSON --> JSON-FG conversion table

Not all the information contained in a CityJSON document can be represented by JSON-FG.
Therefore, some information can be lost in the conversion.
Below is a mapping of the CityJSON concepts to JSON-FG as it is implemented in *cityjson2jsonfg*.

| CityJSON                                                                         | JSON-FG                                                                                                                                                                                                                                                           |
|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Multiple LoDs in one CityObject, each from a different family eg. (0, 1.3, 2.2). | If the CityObject has a geometry with LoD < 0.2, this geometry is assumed to be 2.5D and added as GeoJSON geometry to `"geometry"`. If the rest of the geometries are LoD >= 1, then the geometry with the highest LoD is added as JSON-FG geometry to `"place"`. |
| Multiple LoDs in one CityObject, each from the same family eg. (1.1, 1.3).       | The geometry with the highest LoD is added to the feature.                                                                                                                                                                                                        |
| City model creation date in `CityJSON.metadata.referenceDate`.                   | Assigned as an instant time to `time.date` as `full-date`.                                                                                                                                                                                                        |
| Semantic surfaces                                                                | Not converted.                                                                                                                                                                                                                                                    |
| Appearances                                                                      | Not converted.                                                                                                                                                                                                                                                    |
| Metadata (other than `referenceDate` and `referenceSystem`)                      | Not converted.                                                                                                                                                                                                                                                    |
| CityObject hierarchy (parent and children relations)                             | Not converted.                                                                                                                                                                                                                                                    |

## Communication

All work takes place in the current GitHub repository.
The primary channel for communication is the [GitHub Discussions](https://github.com/3DGI/cityjson2jsonfg/discussions).
Feel free to ask questions you’re wondering about, share ideas and engage with other community members.

## Contributing

Contributions to the project are very welcome!
You could help with testing, documentation, bug reports, bug fixes, implementing new features and more.
Please read the [CONTRIBUTING.md](https://github.com/3DGI/cityjson2jsonfg/blob/master/CONTRIBUTING.md) on how to get started.

## Funding

Version 1.0 was funded by [Geonovum](https://www.geonovum.nl/).