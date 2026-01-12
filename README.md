# Indicators and Dimensions

This is EVERSE repository to maintain a list of Research Software Quality indicators and their corresponding Quality Dimensions.

The metadata for each indicator follows the [RS Quality indicators metadata schema](https://w3id.org/everse/rsqi#). The metadata of each quality dimension follows the [RS Quality dimension metadata schema](https://w3id.org/everse/rsqd#).

A list of indicators supported by EVERSE can be seen at [https://w3id.org/everse/i/indicators/](https://w3id.org/everse/i/indicators/) (e.g., [https://everse.software/indicators/website/indicators.html#no_leaked_credentials](https://everse.software/indicators/website/indicators.html#no_leaked_credentials))

A list of dimensions is available at [https://w3id.org/everse/i/dimensions](https://w3id.org/everse/i/dimensions) (e.g., [https://w3id.org/everse/i/dimensions/functional_suitability](https://w3id.org/everse/i/dimensions/functional_suitability))

## Naming Conventions
All indicators and dimensions follow the naming schema: `https://w3id.org/everse/i/[indicators|dimensions]/{id}`, where `{id}` corresponds to the local identifier of the indicator or dimension. Note: the local identifier corresponds to its `Abbreviation`.


## Content Negotiation
Every indicator is resolvable in a machine-readable manner, using JSON-LD and HTML. For example, the following command:
```
curl -sH "Accept:application/ld+json"  https://w3id.org/everse/i/indicators/persistent_and_unique_identifier -L
```
will yield the description of the corresponding indicator in JSON-LD, while clicking on its URL (i.e., [https://w3id.org/everse/i/indicators/persistent_and_unique_identifier](https://w3id.org/everse/i/indicators/persistent_and_unique_identifier)) will take you to website.


## Contributing new Quality Indicators
If you want to create a new quality indicator, please open a pull request or an issue. 
If you decide to open a pull request, please validate your JSON-LD with an open validator like [the JSON-LD Playground](https://json-ld.org/playground/) to agilize the review. Please make sure your indicator has a source, so we can double check its source and usefulness.


## JSON API Endpoints

The repository provides JSON API endpoints that consolidate all indicators and dimensions for easy consumption by external services. They are produced by the action pipelines when deploying the website.

### Indicators JSON download
- **Endpoint**: https://everse.software/indicators/api/indicators.json
- **Description**: Returns all software quality indicators with metadata
- **Format**: JSON-LD compatible
- **Fields**: 
  - `count`: Total number of indicators
  - `version`: API version
  - `lastUpdated`: Date of last generation (YYYY-MM-DD)
  - `indicators`: Array of all indicator objects

### Dimensions JSON download
- **Endpoint**: https://everse.software/indicators/api/dimensions.json
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
const indicator_response = await fetch('https://everse.software/indicators/api/indicators.json');
const indicator_data = await indicator_response.json();
console.log(`Found ${indicator_data.count} indicators`);

// Fetch all dimensions
const dimension_response = await fetch('https://everse.software/indicators/api/dimensions.json');
const dimension_data = await dimension_response.json();
console.log(`Found ${dimension_data.count} dimensions`);
```

### Generating API Files

The JSON files are automatically generated from the individual JSON files in the `indicators/` and `dimensions/` folders:

```bash
# Generate both APIs
python scripts/generate_api.py

# Generate only indicators API
python scripts/generate_api.py --indicators-only

# Generate only dimensions API
python scripts/generate_api.py --dimensions-only
```

**Note**: The JSON files are generated in `api/` during the GitHub Actions workflow and are automatically served by GitHub Pages at `/api/indicators.json` and `/api/dimensions.json`. They are not committed to the repository to avoid data duplication.

