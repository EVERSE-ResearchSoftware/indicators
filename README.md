# Indicators
A repository to maintain a list of Research Software Quality indicators

The metadata for each indicator follows the [RS Quality indicators metadata schema](https://w3id.org/everse/rsqi#).

A list of indicators supported by EVERSE can be seen in: https://w3id.org/everse/i/indicators/ (e.g., https://everse.software/indicators/website/indicators.html#no_leaked_credentials)

A list of dimensions is available at https://w3id.org/everse/i/dimensions (e.g., https://w3id.org/everse/i/dimensions/functional_suitability)

## API Endpoints

The repository provides JSON API endpoints that consolidate all indicators and dimensions for easy consumption by external services:

### Indicators API
- **Endpoint**: `/api/indicators.json`
- **Description**: Returns all software quality indicators with metadata
- **Format**: JSON-LD compatible
- **Fields**: 
  - `count`: Total number of indicators
  - `version`: API version
  - `lastUpdated`: Date of last generation (YYYY-MM-DD)
  - `indicators`: Array of all indicator objects

### Dimensions API
- **Endpoint**: `/api/dimensions.json`
- **Description**: Returns all software quality dimensions with metadata
- **Format**: JSON-LD compatible
- **Fields**:
  - `count`: Total number of dimensions
  - `version`: API version
  - `lastUpdated`: Date of last generation (YYYY-MM-DD)
  - `dimensions`: Array of all dimension objects

### Usage Example

```javascript
// Fetch all indicators
const response = await fetch('https://your-domain.com/api/indicators.json');
const data = await response.json();
console.log(`Found ${data.count} indicators`);

// Fetch all dimensions
const dimResponse = await fetch('https://your-domain.com/api/dimensions.json');
const dimData = await dimResponse.json();
console.log(`Found ${dimData.count} dimensions`);
```

### Generating API Files

The API files are automatically generated from the individual JSON files in the `indicators/` and `dimensions/` folders:

```bash
# Generate both APIs
python web_generation_scripts/generate_api.py

# Generate only indicators API
python web_generation_scripts/generate_api.py --indicators-only

# Generate only dimensions API
python web_generation_scripts/generate_api.py --dimensions-only
```

**Note**: The API files are generated in `api/` during the GitHub Actions workflow and are automatically served by GitHub Pages at `/api/indicators.json` and `/api/dimensions.json`. They are not committed to the repository to avoid data duplication.

