from io import StringIO
import json


def to_jsonfg(cm):
    out = StringIO()
    jfg = {}
    out.write(json.dumps(jfg, separators=(',', ':')))
    return out
