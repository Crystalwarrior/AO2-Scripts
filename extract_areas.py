import yaml
import sys

def extract_areas_only(input_file, output_file):
    # Load the YAML file
    with open(input_file, 'r') as f:
        data = yaml.safe_load(f)
    
    # Create a new structure with only the areas
    result = {
        'areas': []
    }
    
    # Process each area, keeping only the required fields
    for area in data.get('areas', []):
        filtered_area = {
            'area': area.get('area'),
            'background': area.get('background'),
            'pos_lock': area.get('pos_lock')
        }
        # Only add if all required fields exist
        if all(filtered_area.values()):
            result['areas'].append(filtered_area)
    
    # Write the output
    with open(output_file, 'w') as f:
        yaml.dump(result, f, sort_keys=False, default_flow_style=False, width=float("inf"))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_areas.py input.yaml output.yaml")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    extract_areas_only(input_file, output_file)
    print(f"Filtered YAML written to {output_file}")