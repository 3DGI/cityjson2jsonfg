"""Converter module (convert.py)
Copyright 2022 3DGI <info@3dgi.nl>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from io import StringIO
import json
from copy import deepcopy

import cjio.models
from pyproj import CRS
from click import echo


def to_jsonfg_str(collection):
    out = StringIO()
    out.write(json.dumps(collection, separators=(',', ':')))
    return out


def to_jsonfg_collection(cm):

    link_geojson_collection = {
        "href": "https://geojson.org/schema/FeatureCollection.json",
        "rel": "describedby",
        "type": "application/schema+json",
        "title": "JSON Schema of GeoJSON FeatureCollection"
    }
    link_geojson_feature = {
        "href": "https://geojson.org/schema/Feature.json",
        "rel": "describedby",
        "type": "application/schema+json",
        "title": "JSON Schema of GeoJSON Feature"
    }

    collection = {
        "type": "FeatureCollection",
        "features": [],
        "coordRefSys": None,  # CityJSON:metadata:referenceSystem
        "links": [
            {
                "href": "https://beta.schemas.opengis.net/json-fg/featurecollection.json",
                "rel": "describedby",
                "type": "application/schema+json",
                "title": "JSON Schema of JSON-FG FeatureCollection"
            },
        ]
    }

    feature_template = {
        "id": None,  # CityObject ID
        "type": "Feature",
        "featureType": None,  # CityObject:type mapped to
        "time": None,  # CityJSON:metadata:referenceDate as {"date": referenceDate}
        "properties": None,  # CityObject:attributes
        "geometry": None,  # CityObject:geometry if it has 2.5D representation
        "place": None,  # CityObject:geometry mapped
        "links": [
            {
                "href": "https://beta.schemas.opengis.net/json-fg/feature.json",
                "rel": "describedby",
                "type": "application/schema+json",
                "title": "JSON Schema of JSON-FG Feature"
            },
        ]
    }

    # Convert CityObject --> Feature
    geomdim = set()
    geojson_added = False
    feature_time = cm.j.get("metadata", {}).get("referenceDate", None)
    for coid, co in cm.cityobjects.items():
        feature = deepcopy(feature_template)
        feature["id"] = coid
        feature["featureType"] = co.type
        feature["time"] = {"date": feature_time} if feature_time is not None else None
        feature["properties"] = co.attributes
        convert_boundaries(cm, co, feature, geomdim)
        if feature["geometry"] is not None:
            # A GeoJSON geometry was added by convert_boundaries so we add the schema
            feature["links"].append(link_geojson_feature)
            geojson_added = True
        collection["features"].append(feature)

    # Convert CitJSON --> FeatureCollection
    collection["coordRefSys"] = cm.j.get("metadata", {}).get("referenceSystem", None)
    collection["geometryDimension"] = geomdim.pop() if len(geomdim) == 1 else None
    if geojson_added:
        collection["links"].append(link_geojson_collection)

    return collection


def convert_boundaries(cm, co, feature, geomdim):
    """Convert a CityObject's Geometry to the feature geometry/place.

    Updates the `feature` and populates the `"geometry"` and/or `"place"` members as
    appropriate.

    :param cm: An instance of :class:`cjio.cityjson.CityJSON`.
    :param co: An instance of :class:`cjio.models.CityObject`.
    :param feature: A JSON-FG feature to update.
    :type feature: dict
    :param geomdim: An empty set to be updated. Stores the geometry dimensions of
        the citymodel.
    :type geomdim: set
    """
    max_lod = max(g.lod for g in co.geometry)
    for geom in co.geometry:
        if geom.lod < "0.2":
            crs_to = CRS("OGC:CRS84")
            boundaries_crs84 = geom.reproject(cm.get_epsg(), crs_to=crs_to)
            geom.boundaries = boundaries_crs84
            coordinates = geometry_to_coordinates(geom)
            feature["geometry"] = {"coordinates": coordinates}
            if geom.type == "MultiSurface":
                feature["geometry"]["type"] = "MultiPolygon"
                geomdim.add(2)
            elif geom.type == "MultiPoint":
                feature["geometry"]["type"] = "MultiPoint"
                geomdim.add(0)
            elif geom.type == "MultiLineString":
                feature["geometry"]["type"] = "MultiLineString"
                geomdim.add(1)
            else:
                echo(
                    f"Invalid CityJSON Geometry type {geom.type} for converting to JSON-FG 'geometry', skipping geometry.")
        # We only convert the highest LoD to "place"
        elif geom.lod == max_lod:
            coordinates = geometry_to_coordinates(geom)
            feature["place"] = {"coordinates": coordinates}
            geomdim.add(3)
            if geom.type == "Solid":
                feature["place"]["type"] = "Polyhedron"
            elif geom.type == "MultiSurface":
                feature["place"]["type"] = "MultiPolygon"
            else:
                echo(f"CityJSON Geometry type {geom.type} is not supported for converting to JSON-FG 'place', skipping geometry.")


def geometry_to_coordinates(geometry: cjio.models.Geometry) -> list:
    """Convert a CityJSON Geometry to JSON-FG coordinates."""
    if geometry.type == "Solid":
        return [
            [ [ring + [ring[0], ] for ring in surface] for surface in shell ]
            for shell in geometry.boundaries
        ]
    elif geometry.type == "MultiSurface":
        return [
            [ring + [ring[0], ] for ring in surface]
            for surface in geometry.boundaries
        ]
    elif geometry.type == "MultiPoint" or geometry.type == "MultiLineString":
        return geometry.boundaries
