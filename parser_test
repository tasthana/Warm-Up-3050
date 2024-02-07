import shlex
#import firebase_connection


def get_query():
    query_input = input(">> ")
    return query_input

def parse(query_input):
    if query_input == "help":
        return ["help"], []
    elif query_input == "exit":
        return ["exit"], []

    split_query = shlex.split(query_input)

    if 'where' in split_query:
        if split_query[0] == "get":
            get_list = split_query[1:split_query.index('where')]
            condition_split = split_query[split_query.index('where')+1:]
            if len(get_list) == 0:
                print("ERROR (MISSING ITEMS TO RETRIEVE)")
                return [], []
            elif len(condition_split) == 0:
                print("ERROR (MISSING CONDITIONS)")
                return [], []
        else:
            print("ERROR (MISSING GET)")
            return [], []
    else:
        if split_query[0] == "get":
            get_list = split_query[1:]
            condition_split = []
            if len(get_list) == 0:
                print("ERROR (MISSING ITEMS TO RETRIEVE)")
                return [], []
        else:
            print("ERROR (MISSING GET)")
            return [], []

    keywords = ["make", "model", "color", "msrp", "quantity", "mpg", "horsepower", "*"]
    comparisons = ["=", ">=", "<=", ">", "<"]

    for item in get_list:
        if item in comparisons:
            print("ERROR (MISSING WHERE KEYWORD)")
            return [], []
        if item not in keywords:
            print("ERROR (INVALID KEYWORD IN RETRIEVED ITEMS)")
            return [], []

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

    for item in condition_split:
        if item in comparisons:
            current_element += item
        else:
            current_element += str(item)
            if any(d in current_element for d in comparisons):
                condition_list.append(current_element)
                current_element = ""

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
