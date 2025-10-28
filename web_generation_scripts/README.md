## generate_api.py

This script generates consolidated JSON API endpoint files for both dimensions and indicators from their respective JSON files. The generated files can be served as static API endpoints that external services can fetch.
These files are also used by the website to dynamically load the list of dimensions and indicators.

**Usage:**
```bash
# Generate both API endpoints (dimensions and indicators)
python web_generation_scripts/generate_api.py

# Generate only dimensions API
python web_generation_scripts/generate_api.py --dimensions-only

# Generate only indicators API
python web_generation_scripts/generate_api.py --indicators-only
```

**Output:** 
- `api/dimensions.json` - All dimensions with metadata (version, last update date, count)
- `api/indicators.json` - All indicators with metadata (version, last update date, count)

**Features:**
- Single unified script for both API endpoints
- Reduces code duplication
- Flexible command-line options
- Automatic sorting by name
- Removes unnecessary fields (e.g., "created")
- JSON-LD formatted for semantic web integration