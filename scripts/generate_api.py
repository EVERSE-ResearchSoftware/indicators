#!/usr/bin/env python3
"""
Generate API endpoint JSON files for dimensions and indicators.

This script reads all dimension and indicator JSON files from their respective folders
and creates consolidated JSON files that can be served as API endpoints.

It also enriches indicators with information about tools from the TechRadar repository
that measure or improve each indicator.

Usage:
    python scripts/generate_api.py
    python scripts/generate_api.py --dimensions-only
    python scripts/generate_api.py --indicators-only
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen
from typing import Dict, List, Optional


def load_json_file(filepath):
    """Load and parse a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_json_from_url(url: str) -> Optional[dict]:
    """Fetch and parse JSON from a URL."""
    try:
        with urlopen(url) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"✗ Error fetching {url}: {e}")
        return None


def fetch_techradar_tools() -> Dict[str, dict]:
    """
    Fetch all software tools from the TechRadar repository.

    Returns:
        Dictionary mapping tool IDs to tool data
    """
    print("Fetching TechRadar tools...")
    tools = {}

    # Get list of tool files from GitHub API
    api_url = "https://api.github.com/repos/EVERSE-ResearchSoftware/TechRadar/contents/data/software-tools?ref=main"
    try:
        with urlopen(api_url) as response:
            file_list = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"✗ Error fetching TechRadar file list: {e}")
        return tools

    # Fetch each tool JSON file
    for file_info in file_list:
        if file_info["name"].endswith(".json"):
            download_url = file_info["download_url"]
            tool_data = fetch_json_from_url(download_url)
            if tool_data:
                tool_id = tool_data.get("@id", file_info["name"])
                tools[tool_id] = tool_data
                print(f"✓ Loaded tool: {file_info['name']}")

    print(f"✓ Loaded {len(tools)} tools from TechRadar\n")
    return tools


def normalize_identifier(identifier: str, entity_type: str = "indicator") -> str:
    """
    Normalize entity identifiers to their full URI form.

    Handles two formats:
    - Full URIs: https://w3id.org/everse/i/indicators/... or https://w3id.org/everse/i/dimensions/...
    - Short form: ind:... or dim:...

    Args:
        identifier: The identifier to normalize
        entity_type: Type of entity ("indicator" or "dimension")

    Returns:
        Normalized full URI identifier
    """
    if not identifier:
        return identifier

    # If already a full URI, return as-is
    if identifier.startswith("http"):
        return identifier

    # Handle short form prefixes
    if entity_type == "dimension" and identifier.startswith("dim:"):
        return f"https://w3id.org/everse/i/dimensions/{identifier[4:]}"
    elif entity_type == "indicator" and identifier.startswith("ind:"):
        return f"https://w3id.org/everse/i/indicators/{identifier[4:]}"

    return identifier


def build_entity_to_tools_mapping(tools: Dict[str, dict], property_name: str, entity_type: str = "indicator") -> Dict[str, List[dict]]:
    """
    Build a mapping from entity IDs to tools based on a tool property.

    This is a generic function that can extract any relationship between tools and entities
    (indicators or dimensions) based on a specified property name.

    Args:
        tools: Dictionary mapping tool IDs to tool data
        property_name: Name of the tool property to extract (e.g., "measuresQualityIndicator",
                      "improvesQualityIndicator", "hasQualityDimension")
        entity_type: Type of entity being mapped ("indicator" or "dimension")

    Returns:
        Dictionary mapping entity IDs to lists of tool references
    """
    entity_map: Dict[str, List[dict]] = {}

    for tool_id, tool_data in tools.items():
        refs = tool_data.get(property_name, [])
        if refs and not isinstance(refs, list):
            refs = [refs]

        for ref in refs:
            entity_id = ref.get("@id")
            if entity_id:
                # Normalize the entity ID to full URI form
                entity_id = normalize_identifier(entity_id, entity_type)

                if entity_id not in entity_map:
                    entity_map[entity_id] = []
                entity_map[entity_id].append({"@id": tool_id, "name": tool_data.get("name", tool_id), "@type": "@id"})

    return entity_map


def generate_api(
    source_dir,
    output_file,
    context_url,
    collection_type,
    item_key,
    item_name,
    tool_mappings: Dict[str, Dict[str, List[dict]]] = None,
):
    """
    Generate an API endpoint JSON file.

    Args:
        source_dir: Directory containing source JSON files
        output_file: Path to output API file
        context_url: JSON-LD context URL
        collection_type: Type name for the collection
        item_key: Key name for the items array (e.g., 'dimensions', 'indicators')
        item_name: Human-readable name for items (e.g., 'dimension', 'indicator')
        tool_mappings: Dictionary of tool mappings where keys are field names and values are
                      dictionaries mapping entity IDs to tool lists
                      e.g., {"measuredBy": measures_map, "improvedBy": improves_map, "tools": dimension_tools_map}
    """
    if tool_mappings is None:
        tool_mappings = {}

    # Get all JSON files
    json_files = sorted(source_dir.glob("*.json"))

    if not json_files:
        print(f"⚠ No {item_name} files found in {source_dir}")
        return

    # Load all items
    items = []
    for filepath in json_files:
        try:
            item = load_json_file(filepath)
            # Add the source filename for reference (useful for linking back to GitHub)
            item["_filename"] = filepath.name
            # Remove the "created" field if it exists (not needed in API)
            if "created" in item:
                del item["created"]

            # Add tool mappings to the item if applicable
            entity_id = item.get("@id")
            if entity_id:
                for field_name, mapping in tool_mappings.items():
                    if entity_id in mapping:
                        item[field_name] = mapping[entity_id]

            items.append(item)
            print(f"✓ Loaded: {filepath.name}")
        except Exception as e:
            print(f"✗ Error loading {filepath.name}: {e}")

    # Sort items by name
    items.sort(key=lambda x: x.get("name", ""))

    # Create the API response structure
    api_response = {
        "@context": context_url,
        "@type": collection_type,
        "version": "1.0",
        "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
        "count": len(items),
        item_key: items,
    }

    # Create output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write the output file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(api_response, f, indent=2, ensure_ascii=False)

    print(f"✓ Generated API file: {output_file}")
    print(f"  Total {item_key}: {len(items)}")
    print(f"  Last updated: {api_response['lastUpdated']}\n")


def main():
    """Main function to generate API endpoints."""
    parser = argparse.ArgumentParser(description="Generate API endpoint JSON files")
    parser.add_argument("--dimensions-only", action="store_true", help="Generate only dimensions API")
    parser.add_argument("--indicators-only", action="store_true", help="Generate only indicators API")
    args = parser.parse_args()

    # Define paths
    project_root = Path(__file__).parent.parent
    api_dir = project_root / "api"

    # Fetch TechRadar tools once
    tools = fetch_techradar_tools()

    # Build tool mappings using the generic function
    measures_map = build_entity_to_tools_mapping(tools, "measuresQualityIndicator", entity_type="indicator")
    improves_map = build_entity_to_tools_mapping(tools, "improvesQualityIndicator", entity_type="indicator")
    dimension_tools_map = build_entity_to_tools_mapping(tools, "hasQualityDimension", entity_type="dimension")

    # Determine what to generate
    generate_dimensions = not args.indicators_only
    generate_indicators = not args.dimensions_only

    # Generate dimensions API
    if generate_dimensions:
        print("Generating dimensions API...")
        dimension_mappings = {"tools": dimension_tools_map}
        generate_api(
            source_dir=project_root / "dimensions",
            output_file=api_dir / "dimensions.json",
            context_url="https://w3id.org/everse/rsqd#",
            collection_type="SoftwareQualityDimensionCollection",
            item_key="dimensions",
            item_name="dimension",
            tool_mappings=dimension_mappings,
        )

    # Generate indicators API
    if generate_indicators:
        print("Generating indicators API...")
        indicator_mappings = {"measuredBy": measures_map, "improvedBy": improves_map}
        generate_api(
            source_dir=project_root / "indicators",
            output_file=api_dir / "indicators.json",
            context_url="https://w3id.org/everse/rsqi#",
            collection_type="SoftwareQualityIndicatorCollection",
            item_key="indicators",
            item_name="indicator",
            tool_mappings=indicator_mappings,
        )

    print("✅ API generation complete!")


if __name__ == "__main__":
    main()
