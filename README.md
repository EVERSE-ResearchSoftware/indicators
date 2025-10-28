# Indicators

This is EVERSE repository to maintain a list of Research Software Quality indicators

The metadata for each indicator follows the [RS Quality indicators metadata schema](https://w3id.org/everse/rsqi#).

A list of indicators supported by EVERSE can be seen at [https://w3id.org/everse/i/indicators/](https://w3id.org/everse/i/indicators/) (e.g., [https://everse.software/indicators/website/indicators.html#no_leaked_credentials](https://everse.software/indicators/website/indicators.html#no_leaked_credentials))

A list of dimensions is available at [https://w3id.org/everse/i/dimensions](https://w3id.org/everse/i/dimensions) (e.g., [https://w3id.org/everse/i/dimensions/functional_suitability](https://w3id.org/everse/i/dimensions/functional_suitability))

## API Endpoints

The repository provides JSON API endpoints that consolidate all indicators and dimensions for easy consumption by external services:

### Indicators API
- **Endpoint**: `https://everse.software/indicators/api/indicators.json`
- **Description**: Returns all software quality indicators with metadata
- **Format**: JSON-LD compatible
- **Fields**: 
  - `count`: Total number of indicators
  - `version`: API version
  - `lastUpdated`: Date of last generation (YYYY-MM-DD)
  - `indicators`: Array of all indicator objects

### Dimensions API
- **Endpoint**: `https://everse.software/indicators/api/dimensions.json`
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
const response = await fetch('https://everse.software/indicators/api/indicators.json');
const data = await response.json();
console.log(`Found ${data.count} indicators`);

// Fetch all dimensions
const dimResponse = await fetch('https://everse.software/indicators/api/dimensions.json');
const dimData = await dimResponse.json();
console.log(`Found ${dimData.count} dimensions`);
```

