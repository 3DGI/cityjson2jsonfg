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

You can install *cityjson2jsonfg* with pip.

```shell
pip install cityjson2jsonfg
```

## Usage

Convert a single CityJSON file to JSON-FG.

```shell
cityjson2jsonfg <input.city.json> <output.jsonfg>
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
cjio --suppress_msg <input.city.json> upgrade save stdout | cityjson2jsonfg - <output.jsonfg>
```

## Limitations

Version 1.0 was primarily developed to convert CityJSON files of the [3D BAG](https://3dbag.nl/en/viewer).
Conversion from other data sets might not work.

### Information loss in the CityJSON --> JSON-FG conversion

Not all the information contained in a CityJSON document can be represented by JSON-FG.
Therefore, some information can be lost in the conversion.
Below is a mapping of CityJSON concepts that cannot be directly converted to JSON-FG.

| CityJSON                                                                  | JSON-FG                                                                                                                                                                                                                                                         |
|---------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Multiple LoDs in one CityObject.<br/> Different main levels eg. (0, 1.3, 2.2). | If the CityObject has a geometry with LoD < 1, this geometry is assumed to be 2.5D and added as GeoJSON geometry to `"geometry"`. If the rest of the geometries are LoD >= 1, then the geometry with the highest LoD is added as JSON-FG geometry to `"place"`. |
|                                                                           |                                                                                                                                                                                                                                                                 |
|                                                                           |                                                                                                                                                                                                                                                                 |
|                                                                           |                                                                                                                                                                                                                                                                 |

- multiple LoD
- what is json-fg:time? currently it is cityjson:metadata:referenceDate
- semantic surfaces
- appearances
- metadata
- what about `null` geometries
- object hierarchy?

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