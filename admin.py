# Program starts in this file, get query input and process it
import sys
import json

# (1.7) Write an admin program to load the data from the specified JSON file
def load_data_from_json(json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{json_file}'.")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python admin.py <json_file>")
    else:
        json_file = sys.argv[1]
        data = load_data_from_json(json_file)
        if data:
            print("Data loaded successfully:")
            print(data)