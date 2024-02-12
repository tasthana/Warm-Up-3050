import shlex
#import firebase_connection


def get_query():
    query_input = input(">> ")
    return query_input

def parse(query_input):
    # Process help and exit queries
    if query_input == "help":
        return ["help"], []
    elif query_input == "exit":
        return ["exit"], []

    # Split the query into its individual parts
    split_query = shlex.split(query_input)

    # Check to see if we have the 'where' keyword which would mean that we have conditionals for our output
    if 'where' in split_query:
        # Make sure that the 'get' keyword is in our query so that we know what information to display
        if split_query[0] == "get":
            # Separate our query into the variables we want to display and the conditions for displaying them
            get_list = split_query[1:split_query.index('where')]
            condition_split = split_query[split_query.index('where')+1:]
            if len(get_list) == 0:
                # It wasn't specified which items to get, print an error
                print("ERROR (MISSING ITEMS TO RETRIEVE)")
                return [], []
            elif len(condition_split) == 0:
                # There is nothing after the 'where' keyword, print an error
                print("ERROR (MISSING CONDITIONS)")
                return [], []
        else:
            # The 'get' keyword is missing, print an error
            print("ERROR (MISSING GET)")
            return [], []
    else:
        # We do not have a 'where' keyword, this means that we don't have any conditions for displaying items
        if split_query[0] == "get":
            get_list = split_query[1:]
            condition_split = []
            if len(get_list) == 0:
                # It wasn't specified which items to get, print an error
                print("ERROR (MISSING ITEMS TO RETRIEVE)")
                return [], []
        else:
            # The 'get' keyword is missing, print an error
            print("ERROR (MISSING GET)")
            return [], []

    # These are the valid keywords and comparison operators
    keywords = ["make", "model", "color", "msrp", "quantity", "mpg", "horsepower", "*"]
    comparisons = ["=", ">=", "<=", ">", "<"]

    # Check all items in the list of variables to retrieve to make sure that they are all valid keywords
    for item in get_list:
        if item in comparisons:
            # We are using a comparison before the where keyword, print an error
            print("ERROR (MISSING WHERE KEYWORD)")
            return [], []
        if item not in keywords:
            # We have an invalid keyword in our variables to retrieve, print an error
            print("ERROR (INVALID KEYWORD IN RETRIEVED ITEMS)")
            return [], []

    # Loop through our condition split to make sure it is valid
    for i in range(len(condition_split)):
        if condition_split[i] not in keywords:
            if i % 4 == 0:
                print("ERROR (INVALID KEYWORD IN CONDITIONS)")
                return [], []
            elif i % 4 == 1:
                if condition_split[i] not in comparisons:
                    print("ERROR (INVALID COMPARISON OPERATOR)")
                    return [], []
            elif i % 4 == 3:
                if condition_split[i] != "and":
                    print("ERROR (MISSING AND)")

    condition_list = []
    current_element = ""

    # Turn the comparison split into terms we can query with
    for item in condition_split:
        if item in comparisons:
            current_element += item
        else:
            current_element += str(item)
            if any(d in current_element for d in comparisons):
                condition_list.append(current_element)
                current_element = ""

    # Deal with the 'and' word for if there are multiple conditions
    if len(condition_list) > 1:
        for i in range(len(condition_list)-1):
            if condition_list[i+1][:3] == 'and':
                condition_list[i+1] = condition_list[i+1][3:]
            else:
                print("ERROR (MISSING AND)")
                return [], []
    return get_list, condition_list


def query(get_list, condition_list):
    print("Querying database...")
    print("get_list: ", get_list)
    print("conition_list: ", condition_list)
    #firebase_connection.query(get_list, condition_list)

my_query = ""
#firebase_connection.connect()
while (my_query != "exit"):
    my_query = get_query()
    get_list, condition_list = parse(my_query)
    if get_list != ["help"] and get_list != ["exit"] and get_list != []:
        query(get_list, condition_list)
