def display_menu():
    print("Welcome to the Car Inventory Database.")
    print("Options for queries: \n"
          "Get _ where _ is _ \n"
          "\tExample: Get model where make is Jeep\n"
          "\t*In order to do several conditions, use 'and'\n"
          "\tExample: Get model where make is Jeep and msrp > 30000\n"
          "Add [color] [make] [model] [msrp] [mpg] [horsepower]\n"
          "\tExample: Add white Jeep Cherokee 40000 32.1 87\n"
          "\t*If you want to leave a field blank, say 'NULL'.\n")


def get_input():
    user_input = input("Enter your query or press return to exit: ")
    return user_input


def process_input(user_input):
    if user_input.lower().startswith("get"):
        data = user_input.split(" ")
        num_conditions = data.count("and") + 1  # if the number of ands is zero, there is one condition
        # check to see if query is good, if not return False
        if data[2].lower() != "where" or data[4].lower() != "is":
            print(data)
            print("Invalid query. Format must be 'Get _ where _ is _'")
            return False
        # otherwise query is good
        target = data[1]
        fields = []
        conditions = []
        for i in range(num_conditions):
            fields.append(data[3 + (i * 4)])
            if fields[-1].lower() == "msrp" or fields[-1].lower() == "mpg" or fields[-1].lower() == "horsepower":
                conditions.append(data[4 + (i * 4)] + data[5 + (i * 4)])
                pass
            else:
                conditions.append(data[5 + (i * 4)])
        print(f"Getting {target} where {fields} is/are {conditions}")
        return True
    elif user_input.lower().startswith("add"):
        data = user_input.split(" ")
        # check to see if query is valid, if not return False
        if len(data) != 7:
            print("You must enter a value for every field.")
            return False
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
            return False
        # otherwise query is valid
        print(f"Adding car:\n"
              f"Color: {color}\n"
              f"Make: {make}\n"
              f"Model: {model}\n"
              f"MSRP: ${msrp:,d}\n"
              f"MPG: {mpg:.2f}\n"
              f"Horsepower: {horsepower}\n")
        return True
    # if they enter nothing, exit the program
    elif user_input == "":
        print("Goodbye!")
        return True
    # if it doesn't start with add or get, the query is invalid
    else:
        print("Invalid input")
        return False


if __name__ == "__main__":
    display_menu()
    while True:
        user_input = get_input()
        if process_input(user_input):
            break
