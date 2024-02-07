def menu():
    print("Welcome to the Car Inventory Database.")
    print("Options for queries: \n"
          "Get _ where _ is _ \n"
          "\tExample: Get model where make is Jeep\n"
          "Add [color] [make] [model] [msrp] [mpg] [horsepower]\n"
          "\tExample: Add white Jeep Cherokee 40000 32.1 87\n"
          "\t*If you want to leave a field blank, say 'NULL'.\n")


def get_input():
    user_input = input("Enter your query or press return to exit: ")
    return user_input


def process_input(user_input):
    if user_input.lower().startswith("get"):
        data = user_input.split(" ")
        # check to see if query is good, if not return False
        if len(data) != 6 or data[2].lower() != "where" or data[4].lower() != "is":
            print(data)
            print("Invalid query. Format must be 'Get _ where _ is _'")
            return False
        # otherwise query is good
        target = data[1]
        field = data[3]
        condition = data[5]
        print(f"Getting {target} where {field} is {condition}")
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
    menu()
    while True:
        user_input = get_input()
        if process_input(user_input):
            break
