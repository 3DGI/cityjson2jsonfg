from io import StringIO
import json
from copy import deepcopy


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

    # Convert CitJSON --> FeatureCollection
    collection["coordRefSys"] = cm.j.get("metadata", {}).get("referenceSystem", None)

    # Convert CityObject --> Feature
    feature_time = cm.j.get("metadata", {}).get("referenceDate", None)
    for coid, co in cm.j["CityObjects"].items():
        feature = deepcopy(feature_template)
        feature["id"] = coid
        feature["featureType"] = co["type"]
        feature["time"] = feature_time if feature_time is not None else None
        feature["properties"] = co.get("attributes", None)
        collection["features"].append(feature)

    out = StringIO()
    out.write(json.dumps(collection, separators=(',', ':')))
    return out
