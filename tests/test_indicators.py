import urllib.request, json
from pathlib import Path
from jsonschema import validate
import glob

def test_indicators():
    with urllib.request.urlopen("https://raw.githubusercontent.com/EVERSE-ResearchSoftware/schemas/refs/heads/main/quality_indicators/0.0.1/context.jsonld") as schema_url:
        schema = json.load(schema_url)
        # print("Schema:", json.dumps(schema, indent=2))
        for indicator_file_name in glob.glob("indicators/*.json"):
            print("Validating :", indicator_file_name)
            indicator_instance = json.load(open(indicator_file_name))
            print(validate(instance=indicator_instance, schema=schema))
            assert validate(instance=indicator_instance, schema=schema) is None
