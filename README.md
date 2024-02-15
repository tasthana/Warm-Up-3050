# Car Dealership Inventory Query System

## Description
This project implements a command-line interface for querying the inventory of a car dealership. The dataset is structured around a top-level collection called "cars," 
where each document represents a car in inventory. Each car can have up to seven fields: make, model, color, msrp, quantity, mpg, and horsepower. The "make," "model," 
and "color" fields are strings representing the manufacturer, specific model name, and color of the car, respectively. The "msrp" field represents the listed price of 
the car and is an integer. Optional fields include "mpg" for miles per gallon and "horsepower" for the engine power, both represented as integers. The "quantity" field 
indicates the number of a specific car in inventory.

## Query Language
The query language supports retrieving car information based on various conditions. Here are the options for queries:
- **Get**: Retrieve information based on specified conditions using operators such as '==', '!=', '>=', '<=', '>', '<'. Multiple conditions and fields can be targeted
  using 'and' and commas.
    - Example: `Get model where make is Jeep`
    - Example: `Get model where make == Jeep and msrp > 30000`
    - Example: `Get model,color where make == Jeep and msrp > 30000 and quantity > 0`
- **Add**: Add a new car to the inventory specifying color, make, model, msrp, mpg, and horsepower. Fields can be left blank using 'NULL'.
    - Example: `Add blue Jeep Cherokee 40000 32.1 87`
    - Example: `Add red Ford Mustang 45000 NULL 350`
    - Example: `Add black Toyota Camry 30000 NULL NULL`
- **help**: Display the menu with syntax information and example queries.
- **exit**: Quit the program.
