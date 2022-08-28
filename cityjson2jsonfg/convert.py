from io import StringIO
import json


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

    jfg = {
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

    feature = {
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

    out = StringIO()
    out.write(json.dumps(jfg, separators=(',', ':')))
    return out
