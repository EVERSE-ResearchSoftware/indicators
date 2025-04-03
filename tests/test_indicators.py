import urllib.request, json 
from pathlib import Path
from jsonschema import validate
import glob

def test_indicators():
    indicator_files = []
    with urllib.request.urlopen("https://raw.githubusercontent.com/EVERSE-ResearchSoftware/schemas/refs/heads/main/quality_indicators/0.0.1/context.jsonld") as schema_url:
        schema = json.load(schema_url)
        print("", schema)
        for indicator_file in glob.glob("indicators/*.json"):
            print("Validating :", indicator_file)  
            assert validate(instance=indicator_file, schema=schema) is None
          
