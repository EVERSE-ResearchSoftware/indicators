#!/usr/bin/env python3
"""
Generate API endpoint JSON files for dimensions and indicators.

This script reads all dimension and indicator JSON files from their respective folders
and creates consolidated JSON files that can be served as API endpoints.

Usage:
    python scripts/generate_api.py
    python scripts/generate_api.py --dimensions-only
    python scripts/generate_api.py --indicators-only
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


def load_json_file(filepath):
    """Load and parse a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
    
    
def collect_indicator_dimensions(item, filename, dimension_map):
    """
    Collect indicator filenames per dimension.
    """

    quality_dimensions = item.get("qualityDimension", [])

    if isinstance(quality_dimensions, dict):
        quality_dimensions = [quality_dimensions]

    indicator_name = Path(filename).stem

    for dimension in quality_dimensions:
        dimension_id = dimension.get("@id", "")

        if dimension_id:
            dimension_name = dimension_id.rstrip('/').split('/')[-1]

            if dimension_name not in dimension_map:
                dimension_map[dimension_name] = []

            if indicator_name not in dimension_map[dimension_name]:
                dimension_map[dimension_name].append(indicator_name)


def write_dimension_counts(dimension_map):
    """
    Write indicator counts per dimension to a JSON file.
    """

    output_file = (Path(__file__).parent.parent / "website" / "utils" / "indicators_per_dimension.json")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dict(dimension_map.items()), f, indent=2, ensure_ascii=False)

    print(f"✓ Generated indicators per dimension file: "f"{output_file}")
    

def generate_api(source_dir, output_file, context_url, collection_type, item_key, item_name):
    """
    Generate an API endpoint JSON file.
    
    Args:
        source_dir: Directory containing source JSON files
        output_file: Path to output API file
        context_url: JSON-LD context URL
        collection_type: Type name for the collection
        item_key: Key name for the items array (e.g., 'dimensions', 'indicators')
        item_name: Human-readable name for items (e.g., 'dimension', 'indicator')
    """
    # Get all JSON files
    json_files = sorted(source_dir.glob('*.json'))
    
    if not json_files:
        print(f"⚠ No {item_name} files found in {source_dir}")
        return
    
    # Load all items
    items = []

    # Counter for dimensions
    dimension_indicators = {}

    for filepath in json_files:
        try:
            item = load_json_file(filepath)

            # Add the source filename for reference
            item['_filename'] = filepath.name

            # Remove the "created" field if it exists
            if 'created' in item:
                del item['created']

            # Count indicator dimensions
            if source_dir.parts[-1] == "indicators":
                collect_indicator_dimensions(item, filepath.name, dimension_indicators)

            items.append(item)

            print(f"✓ Loaded: {filepath.name}")

        except Exception as e:
            print(f"✗ Error loading {filepath.name}: {e}")
            
    write_dimension_counts(dimension_indicators)
    
    # Sort items by name
    items.sort(key=lambda x: x.get('name', ''))
    
    # Create the API response structure
    api_response = {
        "@context": context_url,
        "@type": collection_type,
        "version": "1.0",
        "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
        "count": len(items),
        item_key: items
    }
    
    # Create output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(api_response, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Generated API file: {output_file}")
    print(f"  Total {item_key}: {len(items)}")
    print(f"  Last updated: {api_response['lastUpdated']}\n")


def main():
    """Main function to generate API endpoints."""
    parser = argparse.ArgumentParser(description='Generate API endpoint JSON files')
    parser.add_argument('--dimensions-only', action='store_true', 
                       help='Generate only dimensions API')
    parser.add_argument('--indicators-only', action='store_true',
                       help='Generate only indicators API')
    args = parser.parse_args()
    
    # Define paths
    project_root = Path(__file__).parent.parent
    api_dir = project_root / 'api'
    
    # Determine what to generate
    generate_dimensions = not args.indicators_only
    generate_indicators = not args.dimensions_only
    
    # Generate dimensions API
    if generate_dimensions:
        print("Generating dimensions API...")
        generate_api(
            source_dir=project_root / 'dimensions',
            output_file=api_dir / 'dimensions.json',
            context_url="https://w3id.org/everse/rsqd#",
            collection_type="SoftwareQualityDimensionCollection",
            item_key="dimensions",
            item_name="dimension"
        )
    
    # Generate indicators API
    if generate_indicators:
        print("Generating indicators API...")
        generate_api(
            source_dir=project_root / 'indicators',
            output_file=api_dir / 'indicators.json',
            context_url="https://w3id.org/everse/rsqi#",
            collection_type="SoftwareQualityIndicatorCollection",
            item_key="indicators",
            item_name="indicator"
        )
    
    print("✅ API generation complete!")


if __name__ == '__main__':
    main()
