import firebase_connection as fbc
import shlex
from car import Car

def display_menu():
    """
    This function displays a help menu to the user
    """
    print("=============================================================================================\n"
          "Welcome to the Car Inventory Database.\n"
          "=============================================================================================\n"
          "Options for queries: \n"
          ">  Get _ where _ (and _ ...) \n"
          "     - Example: Get model where make == Jeep\n"
          "   In order to do several conditions, use 'and'\n"
          "     - Example: Get model where make == Jeep and msrp > 30000\n"
          "   In order to target several categories, use a comma (but no spaces) or '*'\n"
          "     - Example: Get model,color where make == Jeep and msrp > 30000\n"
          "     - Example: Get * where make == Jeep and msrp > 30000\n"
          "   The valid fields are 'make', 'model', 'color', 'quantity', 'msrp', 'mpg', 'horsepower'\n"
          "   The valid operators are '==', '!=', '>=', '<=', '>', '<'\n"
          "=============================================================================================\n"
          ">  Add [color] [make] [model] [msrp] [mpg] [horsepower]\n"
          "     - Example: Add blue Jeep Cherokee 40000 32.1 87\n"
          "   If you want to leave optional fields mpg and/or horsepower blank, say 'NULL'.\n"
          "     - Example: Add red Ford Mustang 45000 NULL 350\n"
          "     - Example: Add black Toyota Camry 30000 NULL NULL\n"
          "Type 'help' to see the menu again.\n"
          "Enter 'exit' to quit.\n")


def get_input():
    """
    This function is used to get input for a query from the user.

    :return: a string representation of the user's input
    """

    user_input = input(">> ")
    return user_input


def process_input(user_input):
    """
    This function takes in a user's query as a string and parses
    it to get the variables that the user wants to retrieve and
    the conditions for retrieval.

    :param user_input: the user's query as a string
    :return: true if valid query, false otherwise
    """

    if user_input.lower().startswith("get"):
        data = shlex.split(user_input.rstrip())
        num_conditions = data.count("and") + 1  # if the number of ands is zero, there is one condition
        operators = ['==', '!=', '<', '>', '<=', '>=']
        keywords = ["make", "model", "color", "msrp", "quantity", "mpg", "horsepower"]
        # check to see if query is good, if not return False
        if len(data) < 6 or data[2].lower() != "where" or (data[4].lower() != "is" and data[4] not in operators):
            print("Invalid format for a Get query. Type 'help' to see the available operations.")
            return []
        # otherwise query is good
        targets = data[1].split(',')  # split so that multiple targets can be fetched
        fields = []
        operands = []
        conditions = []
        for i in range(num_conditions):
            if data[3 + (i * 4)] in keywords:
                fields.append(data[3 + (i * 4)])
            else:
                print(f"{data[3 + (i * 4)]} is not a valid keyword. Type 'help' to see the available operations.")
                return []
            if fields[-1].lower() == "msrp" or fields[-1].lower() == "mpg" or fields[-1].lower() == "horsepower" or fields[-1].lower() == "quantity":
                operands.append(data[4 + (i * 4)])
                try:
                    conditions.append(float(data[5 + (i * 4)]))
                except ValueError:
                    print(f"{data[3 + (i * 4)]} must be a number. Type 'help' to see the available operations.")
                    return []
            else:
                if data[4 + (i * 4)] == ">" or data[4 + (i * 4)] == "<" or data[4 + (i * 4)] == ">=" or data[4 + (i * 4)] == "<=":
                    print(f"Cannot use numerical comparisons on {data[3 + (i * 4)]}. Type 'help' to see the available operations.")
                    return []
                operands.append(data[4 + (i * 4)])
                conditions.append(data[5 + (i * 4)])
        query_list = []
        for i in range(len(conditions)):
            query_list.append([fields[i], operands[i], conditions[i]])

        return [targets, query_list]
    elif user_input.lower().startswith("add"):
        data = shlex.split(user_input.rstrip())
        # check to see if query is valid, if not return False
        if len(data) != 7:
            print(data)
            print("You must enter a value for every field. Type 'help' to see the available operations.")
            return []
        # otherwise query format is good
        color = data[1]
        make = data[2].capitalize()
        model = data[3].capitalize()
        # make sure msrp, mpg, horsepower are numbers, if not, return false
        try:
            msrp = int(data[4])
            if data[5].lower() != "null":
                mpg = float(data[5])
            else:
                mpg = None
            if data[6].lower() != "null":
                horsepower = int(data[6])
            else:
                horsepower = None
        except ValueError:
            print("MSRP, miles per gallon, and horsepower must all be numbers (mpg and horsepower can also be NULL). Type 'help' to see the available operations.")
            return []
        # otherwise query is valid
        return [make, model, color, msrp, mpg, horsepower]
    # if they enter exit, exit the program
    elif user_input == "exit":
        print("Goodbye!")
        return [1]
    # if it doesn't start with add or get, the query is invalid
    elif user_input.lower() == "help":
        display_menu()
        return []
    else:
        print("Invalid input. Type 'help' to see the available operations.")
        return []


# executes query
def execute_query(ref, retrieval_list, condition_list):
    """
    This function takes in a database record, the list of variables to retrieve,
    and the list of conditions for returned items, and it executes queries to
    retrieve data from the firebase datstore referenced.

    :param ref: the reference to the datastore
    :param retrieval_list: the list of variables to retrieve
    :param condition_list: the list of conditions to be used in queries
    :return: a list of dictionaries representing the data retreived from firebase
    """

    # Create an empty list to store our results
    results = []

    # if the retrieval list contains '*' then we want to retrieve all variables
    if '*' in retrieval_list:
        retrieval_list = ["make", "model", "color", "msrp", "quantity", "mpg", "horsepower"]

    # We are actually splitting this query up into multiple queries, one for each condition in condition_list
    # This performs the first query
    if len(condition_list) > 0:
        try:
            # query the database
            output = fbc.query_database(ref, retrieval_list, condition_list[0][0], condition_list[0][1],
                                        condition_list[0][2])
            # add our output to the results list
            for element in output:
                results.append(element.to_dict())
        except:
            # Something went wrong while processing the query, let the user know
            print("Query failed to process")
            return None
    else:
        try:
            # query the database
            output = fbc.query_database(ref, retrieval_list)
            # add our output to the results list
            for element in output:
                results.append(element.to_dict())
        except:
            # Something went wrong while processing the query, let the user know
            print("Query failed to process")
            return None

    # This performs the rest of the queries (if there are any others)
    if len(condition_list) > 1:
        for condition in condition_list[1:]:
            try:
                # query the database
                output = fbc.query_database(ref, retrieval_list, condition[0], condition[1], condition[2])
                # convert the output to a list of dictionaries
                output_list = []
                for element in output:
                    output_list.append(element.to_dict())
                # Perform AND operation
                results = [x for x in results if x in output_list]

            except:
                # Something went wrong while processing the query, let the user know
                print("Query failed to process2")
                return None

    return results

def display_query_output(query_output):
    """
    This function displays the output from a query in a formatted way.

    :param query_output: A list of dictionaries to display
    """
    print(f"Query returned {len(query_output)} result(s):")
    print("\t---------------------")
    keywords = ["Make", "Model", "Color", "Msrp", "Quantity", "Mpg", "Horsepower"]
    for car_dict in query_output:
        for word in keywords:
            if word.lower() in car_dict:
                print(f"\t{word}: {car_dict.get(word.lower())}")
        print("\t---------------------")

def add_to_database(ref, parsed_query):
    """
    This function adds a new car to the database

    :param ref: the reference to the datastore
    :param parsed_query: the parsed query of fields for the new car
    """
    result = execute_query(ref, ["*"], [['make', '==', parsed_query[0]], ['model', '==', parsed_query[1]], 
                                                         ['color', '==', parsed_query[2]], ['msrp', '==', parsed_query[3]], 
                                                         ['mpg', '==', parsed_query[4]], ['horsepower', '==', parsed_query[5]]])
    if len(result) > 0:
        print("This car is already in the database")
        return None
    else:
        new_car = Car(parsed_query[0], parsed_query[1], parsed_query[2], parsed_query[3], 1, parsed_query[4], parsed_query[5])
        fbc.set_collection_element(dealership_ref, new_car)
        print("Car has been added to database")
        return new_car


if __name__ == "__main__":
    print("\nConnecting to firebase...")
    client = fbc.verify_connection('warm-up-project-3050.json')
    dealership_ref = fbc.retrieve_reference(client, "3050-Dealership")
    print("Connected to firebase successfully!\n")

    display_menu()

    # Loop until the user decides to exit
    while True:
        # get the input from the user
        user_input = get_input()
        # parse the query
        parsed_query = process_input(user_input)

        # make sure the user entered a valid query before continuing
        if parsed_query != []:
            # The user wants to quit
            if parsed_query == [1]:
                break
            if len(parsed_query) == 2:      # The query is a 'get' query
                results = execute_query(dealership_ref, parsed_query[0], parsed_query[1])
                print()
                display_query_output(results)
            elif len(parsed_query) == 6:    # The query is an 'add' query
                new_car = add_to_database(dealership_ref, parsed_query)
                if new_car:
                    display_query_output([new_car.to_dict()])
