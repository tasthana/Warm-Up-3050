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
                    if 'mpg' in car_dict and 'horsepower' in car_dict:
                        car_list.append(Car(car_dict.get('uuid'), car_dict.get('make'), car_dict.get('model'), 
                                            car_dict.get('color'), car_dict.get('msrp'), car_dict.get('quantity'),
                                            mpg=car_dict.get('mpg'), horsepower=car_dict.get('horsepower')))
                    elif 'mpg' in car_dict:
                        car_list.append(Car(car_dict.get('uuid'), car_dict.get('make'), car_dict.get('model'), 
                                            car_dict.get('color'), car_dict.get('msrp'), car_dict.get('quantity'),
                                            mpg=car_dict.get('mpg')))
                    elif 'horsepower' in car_dict:
                        car_list.append(Car(car_dict.get('uuid'), car_dict.get('make'), car_dict.get('model'), 
                                            car_dict.get('color'), car_dict.get('msrp'), car_dict.get('quantity'),
                                            horsepower=car_dict.get('horsepower')))
                    else:
                        car_list.append(Car(car_dict.get('uuid'), car_dict.get('make'), car_dict.get('model'), 
                                            car_dict.get('color'), car_dict.get('msrp'), car_dict.get('quantity')))
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
        car_list = load_data_from_json(json_file)
        if car_list != None:
            print("Data loaded from file successfully")
            print("Connecting to firebase...")
            # client = fb.verify_connection('warm-up-project-3050.json')
            # dealership_ref = fb.retrieve_reference("3050-Dealership", client)
            for car in car_list:
                print(car.to_dict())
                # dealership_ref.document(car.uuid).set(
                #     car.to_dict()
                # )
