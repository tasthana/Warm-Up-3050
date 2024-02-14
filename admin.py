import sys
import json
import car
import firebase_connection as fbc
from car import Car


def load_data_from_json(json_file):
    """
    This funciton loads data from a json file and returns a list of Car objects.

    :param json_file: the name of a JSON file
    :return: a list of car objects
    """
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
            client = fbc.verify_connection('warm-up-project-3050.json')
            dealership_ref = fbc.retrieve_reference(client, "3050-Dealership")
            print("Connected to firebase successfully")
            print("Uploading data to firebase...")
            for element in car_list:
                fbc.set_collection_element(dealership_ref, element)
            print(f"Successfully uploaded {len(car_list)} entries to firebase")
            # fb.print_collection(dealership_ref)
        else:
            print(f"Unable to load data from '{json_file}'.")
