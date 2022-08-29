from cityjson2jsonfg import convert

def test_to_jsonfg_collection(input_model_5907):
    re = convert.to_jsonfg_collection(input_model_5907)
    assert len(re["features"]) == 887