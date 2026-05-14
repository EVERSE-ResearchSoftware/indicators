## generate_api.py

This script generates consolidated JSON API endpoint files for both dimensions and indicators from their respective JSON files. The generated files can be served as static API endpoints that external services can fetch.
These files are also used by the website to dynamically load the list of dimensions and indicators.

The script also enriches both dimensions and indicators with tool information from the TechRadar repository, showing which tools measure, improve, or address each quality dimension/indicator.

**Usage:**
```bash
# Generate both API endpoints (dimensions and indicators)
python scripts/generate_api.py

# Generate only dimensions API
python scripts/generate_api.py --dimensions-only

# Generate only indicators API
python scripts/generate_api.py --indicators-only
```

**Output:** 
- `api/dimensions.json` - All dimensions with metadata, including associated tools
- `api/indicators.json` - All indicators with metadata, including associated tools

**Features:**
- Single unified script for both API endpoints
- Reduces code duplication through generic mapping functions
- Flexible command-line options
- Automatic sorting by name
- Removes unnecessary fields (e.g., "created")
- JSON-LD formatted for semantic web integration
- **Integrates tools from TechRadar repository:**
  - Enriches dimensions with tools that address them (via `hasQualityDimension`)
  - Enriches indicators with tools that measure them (via `measuresQualityIndicator`)
  - Enriches indicators with tools that improve them (via `improvesQualityIndicator`)

### Tool Integration

The script automatically fetches all tools from the [TechRadar repository](https://github.com/EVERSE-ResearchSoftware/TechRadar) and builds relationships:

**For Dimensions:**
- Adds a `tools` array listing all tools that address/support this dimension

**For Indicators:**
- Adds a `measuredBy` array with tools that measure/assess this indicator
- Adds an `improvedBy` array with tools that help improve/achieve this indicator

Each tool reference includes:
- `@id`: The unique identifier of the tool
- `name`: The human-readable name of the tool
- `@type`: "@id" (JSON-LD type indicator)