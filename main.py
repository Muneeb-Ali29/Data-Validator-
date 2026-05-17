
import argparse
import json
from pathlib import Path
from models import Config, Product
from pydantic import ValidationError

def main():
    parser = argparse.ArgumentParser(description="Strict Config & Data Validator CLI")
    parser.add_argument("data_file", help="Path to the JSON data file")
    args = parser.parse_args()

    # Load and validate Environment Config
    try:
        print("Loading environment configuration...")
        config = Config()
        print(f"Configuration loaded successfully: DEBUG_MODE={config.DEBUG_MODE}")
        # Only print part of the API key for security
        masked_key = config.API_KEY[:4] + "***" if len(config.API_KEY) > 4 else "***"
        if config.DEBUG_MODE:
            print(f"API_KEY is configured (starts with {masked_key})")
    except ValidationError as e:
        print("Configuration validation failed!")
        print(e)
        return

    # Read JSON Data File
    data_path = Path(args.data_file)
    if not data_path.exists():
        print(f"Error: The file {args.data_file} does not exist.")
        return
        
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return

    if not isinstance(data, list):
        print("Error: JSON data should be a list of products.")
        return

    # Validate Data
    print(f"\nValidating {len(data)} products from {args.data_file}...")
    valid_products = []
    errors = []

    for idx, item in enumerate(data):
        try:
            product = Product(**item)
            valid_products.append(product)
        except ValidationError as e:
            errors.append({"index": idx, "item": item, "errors": e.errors()})

    # Print Summary
    print("\n--- Validation Summary ---")
    print(f"Total processed : {len(data)}")
    print(f"Valid products  : {len(valid_products)}")
    print(f"Invalid products: {len(errors)}")

    if errors:
        print("\n--- Validation Errors ---")
        for err in errors:
            print(f"Product at index {err['index']} failed:")
            for detail in err['errors']:
                field_name = ".".join(map(str, detail["loc"]))
                print(f"  - Field '{field_name}': {detail['msg']}")

if __name__ == "__main__":
    main()
