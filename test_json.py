import pytest
import json

def test_load_json_string_from_file():
    seed_data='ships_full.json'
    with open(seed_data, "r") as seed_content: 
        json_string = seed_content.read()
    t = type(json_string)
    assert  str(t).startswith ("<class 'str'")
        
    
def test_loads():
    seed_data='ships_full.json'
    with open(seed_data, "r") as seed_content: 
        json_string = seed_content.read()
    json_list = json.loads(json_string)
    assert len(json_list) == 33
