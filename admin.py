# Program starts in this file, get query input and process it
import sys
import json
import car
import firebase_connection as fb
from car import Car


# (1.7) Write an admin program to load the data from the specified JSON file
def load_data_from_json(json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            car_list = []
            if data:
                for car_dict in data:
                    car_list.append(Car.from_dict(car_dict))
                return car_list
            else:
                return None
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
        car_list = load_data_from_json(json_file)
        if car_list != None:
            print("Data loaded from file successfully")
            print("Connecting to firebase...")
            client = fb.verify_connection('warm-up-project-3050.json')
            dealership_ref = fb.retrieve_reference("3050-Dealership", client)
            print("Connected to firebase successfully")
            print("Uploading data to firebase...")
            for element in car_list:
                dealership_ref.document(str(element.uuid)).set(
                    element.to_dict()
                )
            print(f"Successfully uploaded {len(car_list)} entries to firebase")
            # fb.print_collection(dealership_ref)
        else:
            print(f"Unable to load data from '{json_file}'.")
