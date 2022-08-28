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

## Limitations

Version 1.0 was primarily developed to convert CityJSON files of the [3D BAG](https://3dbag.nl/en/viewer).
Conversion from other data sets might not work.

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