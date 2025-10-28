#!/usr/bin/env python3
"""
Generate API endpoint JSON file for dimensions.

This script reads all dimension JSON files from the dimensions/ folder
and creates a consolidated JSON file that can be served as an API endpoint.

Usage:
    python web_generation_scripts/generate_dimensions_api.py
"""

import json
from datetime import datetime
from pathlib import Path


def load_dimension_file(filepath):
    """Load and parse a dimension JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_dimensions_api():
    """Generate the dimensions API JSON file."""
    # Define paths
    project_root = Path(__file__).parent.parent
    dimensions_dir = project_root / 'dimensions'
    output_dir = project_root / 'website' / 'api'
    output_file = output_dir / 'dimensions.json'
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all dimension JSON files
    dimension_files = sorted(dimensions_dir.glob('*.json'))
    
    if not dimension_files:
        print(f"No dimension files found in {dimensions_dir}")
        return
    
    # Load all dimensions
    dimensions = []
    for filepath in dimension_files:
        try:
            dimension = load_dimension_file(filepath)
            # Remove the "created" field if it exists (not needed in API)
            if 'created' in dimension:
                del dimension['created']
            dimensions.append(dimension)
            print(f"✓ Loaded: {filepath.name}")
        except Exception as e:
            print(f"✗ Error loading {filepath.name}: {e}")
    
    # Sort dimensions by name
    dimensions.sort(key=lambda x: x.get('name', ''))
    
    # Create the API response structure
    api_response = {
        "@context": "https://w3id.org/everse/rsqd#",
        "@type": "SoftwareQualityDimensionCollection",
        "version": "1.0",
        "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
        "count": len(dimensions),
        "dimensions": dimensions
    }
    
    # Write the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(api_response, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Generated API file: {output_file}")
    print(f"  Total dimensions: {len(dimensions)}")
    print(f"  Last updated: {api_response['lastUpdated']}")


if __name__ == '__main__':
    generate_dimensions_api()
