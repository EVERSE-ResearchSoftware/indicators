import os
import json

dir = 'dimensions'
dimensions = []

for file in os.listdir(dir):
    path = os.path.join(dir, file)

    if os.path.isfile(path) and file.endswith('.json'):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            if "@graph" in data:
                for item in data["@graph"]:
                    item.pop("@context", None)
                    dimensions.append(item)
            else:
                data.pop("@context", None)
                dimensions.append(data)

json_ld = {
    "@context": "https://w3id.org/everse/rsqi#",
    "@graph": dimensions
}

with open('dimensions.json', 'w', encoding='utf-8') as f_out:
    json.dump(json_ld, f_out, ensure_ascii=False, indent=2)
