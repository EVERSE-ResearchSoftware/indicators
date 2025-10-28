## generate_lists.py

This script is used to update the list of json files located in both the indicators and dimensions directories in order to make the website show its table with its content up to date.

## indicator_append.py

This script is used to append the different indicators located in each json file into a single json-ld.

## dimension_append.py

Similarly, this script does the same as the indicator_append.py script but with the dimensions.

## generate_dimensions_api.py

This script generates a consolidated JSON API endpoint file (`website/api/dimensions.json`) from all dimension JSON files in the `dimensions/` folder. The generated file can be served as a static API endpoint that external services can fetch to retrieve the complete list of software quality dimensions.

**Usage:**
```bash
python web_generation_scripts/generate_dimensions_api.py
```

**Output:** `website/api/dimensions.json` - A JSON file containing all dimensions with metadata including version, last update date, and total count.