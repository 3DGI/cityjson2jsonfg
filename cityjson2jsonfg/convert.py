from io import StringIO
import json
from copy import deepcopy

from pyproj import CRS


def to_jsonfg(cm):

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
    feature_time = cm.j.get("metadata", {}).get("referenceDate", None)
    for coid, co in cm.cityobjects.items():
        feature = deepcopy(feature_template)
        feature["id"] = coid
        feature["featureType"] = co.type
        feature["time"] = {"date": feature_time} if feature_time is not None else None
        feature["properties"] = co.attributes
        # TODO: generalize this for other cityobject types
        if len(co.geometry) > 0 and (co.type == "Building" or co.type == "BuildingPart"):
            for geom in co.geometry:
                if geom.lod < "1":
                    crs_to = CRS("OGC:CRS84")
                    boundaries_crs84 = geom.reproject(cm.get_epsg(), crs_to=crs_to)
                    feature["geometry"] = {"coordinates": boundaries_crs84}
                    if geom.type == "MultiSurface":
                        feature["geometry"]["type"] = "MultiPolygon"
                        geomdim.add(2)
                    elif geom.type == "MultiPoint":
                        feature["geometry"]["type"] = "MultiPoint"
                        geomdim.add(0)
                    elif geom.type == "MultiLineString":
                        feature["geometry"]["type"] = "MultiLineString"
                        geomdim.add(1)
                # We only convert LoD2 (or higher) Building geometries to "place"
                elif geom.lod > "1":
                    feature["place"] = {"coordinates": geom.boundaries}
                    geomdim.add(3)
                    if geom.type == "Solid":
                        feature["place"]["type"] = "Polyhedron"
                    elif geom.type == "MultiSurface":
                        feature["place"]["type"] = "MultiPolygon"
        collection["features"].append(feature)

    # Convert CitJSON --> FeatureCollection
    collection["coordRefSys"] = cm.j.get("metadata", {}).get("referenceSystem", None)
    collection["geometryDimension"] = geomdim.pop() if len(geomdim) == 1 else None

    out = StringIO()
    out.write(json.dumps(collection, separators=(',', ':')))
    return out
