import firebase_connection as fbc
import shlex


def display_menu():
    """
    This function displays a help menu to the user
    """
    print("======================================\n"
          "Welcome to the Car Inventory Database.\n"
          "======================================\n"
          "Options for queries: \n"
          "Get _ where _ is _ \n"
          "\tExample: Get model where make is Jeep\n"
          " - In order to do several conditions, use 'and'\n"
          "\tExample: Get model where make is Jeep and msrp > 30000\n"
          " - In order to target several categories, use a comma\n"
          "\tExample: Get model,color where make is Jeep and msrp > 30000\n"
          "======================================================================\n"
          "Add [color] [make] [model] [msrp] [mpg] [horsepower]\n"
          "\tExample: Add white Jeep Cherokee 40000 32.1 87\n"
          " - If you want to leave a field blank, say 'NULL'.\n"
          "Type 'help' to see the menu again.")


def get_input():
    """
    This function is used to get input for a query from the user.

    :return: a string representation of the user's input
    """

    user_input = input("Enter your query or press return to exit: ")
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
        data = shlex.split(user_input)
        num_conditions = data.count("and") + 1  # if the number of ands is zero, there is one condition
        # check to see if query is good, if not return False
        operators = ['==', '<', '>', '<=', '>=']
        if data[2].lower() != "where" or (data[4].lower() != "is" and data[4] not in operators):
            print(data)
            print("Invalid query. Format must be 'Get _ where _ is _'")
            return []
        # otherwise query is good
        targets = data[1].split(',')  # split so that multiple targets can be fetched
        fields = []
        operands = []
        conditions = []
        for i in range(num_conditions):
            fields.append(data[3 + (i * 4)])
            if fields[-1].lower() == "msrp" or fields[-1].lower() == "mpg" or fields[-1].lower() == "horsepower":
                operands.append(data[4 + (i * 4)])
                conditions.append(data[5 + (i * 4)])
            else:
                operands.append("==")
                conditions.append(data[5 + (i * 4)])
        print(f"Getting {targets} where {fields} is {conditions}")
        query_list = []
        for i in range(len(conditions)):
            query_list.append([fields[i], operands[i], conditions[i]])

        return [targets, query_list]
    elif user_input.lower().startswith("add"):
        data = user_input.split(" ")
        # check to see if query is valid, if not return False
        if len(data) != 7:
            print("You must enter a value for every field.")
            return []
        # otherwise query format is good
        color = data[1]
        make = data[2].capitalize()
        model = data[3].capitalize()
        # make sure msrp, mpg, horsepower are numbers, if not, return false
        try:
            msrp = int(data[4])
            mpg = float(data[5])
            horsepower = int(data[6])
        except ValueError:
            print("MSRP, miles per gallon, and horsepower must all be numbers.")
            return []
        # otherwise query is valid
        print(f"Adding car:\n"
              f"Color: {color}\n"
              f"Make: {make}\n"
              f"Model: {model}\n"
              f"MSRP: ${msrp:,d}\n"
              f"MPG: {mpg:.2f}\n"
              f"Horsepower: {horsepower}\n")
        return [make, model, color, msrp, mpg, horsepower]
    # if they enter nothing, exit the program
    elif user_input == "":
        print("Goodbye!")
        return [1]
    # if it doesn't start with add or get, the query is invalid
    elif user_input.lower() == "help":
        display_menu()
    else:
        print("Invalid input")
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
    print(f"Query returned {len(query_output)} results:")
    keywords = ["Make", "Model", "Color", "Msrp", "Quantity", "Mpg", "Horsepower"]
    for car_dict in query_output:
        for word in keywords:
            if word.lower() in car_dict:
                print(f"\t{word}: {car_dict.get(word.lower())}")
        print()


if __name__ == "__main__":
    print("Connecting to firebase...")
    client = fbc.verify_connection('warm-up-project-3050.json')
    dealership_ref = fbc.retrieve_reference(client, "3050-Dealership")
    print("Connected to firebase successfully!\n")
    # test_result = execute_query(dealership_ref, ['make', 'model', 'msrp', 'mpg'], [['mpg', '>', 26]])
    # display_query_output(test_result)
    # test_result2 = execute_query(dealership_ref, ['make'], [])
    # print(test_result2)
    display_menu()
    print()
    while True:
        user_input = get_input()
        if user_input == '':
            break
        parsed_query = process_input(user_input)
        if parsed_query != []:
            results = execute_query(dealership_ref, parsed_query[0], parsed_query[1])
            print("PARSED QUERY[0]: ", parsed_query[0])
            print("PARSED QUERY[1]: ", parsed_query[1])
            display_query_output(results)
