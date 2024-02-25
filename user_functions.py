import messages


# ~~~~~~~~~~~~~~~~ SIGN UP/STAFF REGISTRATION ~~~~~~~~~~~~~~~~
def sign_up(users_dict, current_username, current_user_role):
    # entering the valid username
    while True:
        username = input("\nEnter username: ")
        if username == '\n' or len(username) == 0 or username.isspace():
            print("Wrong input.\n")
        elif username not in users_dict.keys():
            break
        elif username in users_dict.keys():
            print("Username already in use...\n")

    # entering the valid password
    while True:
        password = input("Type in your new password: ")
        if has_numbers(password) and len(password) >= 6:
            break
        else:
            print("Password must contain a number, and must be 6+ characters long!\n")

    # entering the first name
    while True:
        first_name = input("Set your desirable name: ")
        if first_name == '\n' or len(first_name) == 0 or first_name.isspace():
            print("Wrong input.\n")
        else:
            break

    # entering the last name
    while True:
        last_name = input("Set your desirable surname: ")
        if last_name == '\n' or len(last_name) == 0 or last_name.isspace():
            print("Wrong input.\n")
        else:
            break

    # role assignment
    if current_user_role[0] == 'manager':
        print("What role will he/she have? ")
        print("[1] MANAGER")
        print("[2] SELLER")
        while True:
            input_value = input("> ")
            if input_value == "1":
                role = "manager"
                break
            elif input_value == "2":
                role = "seller"
                break
            else:
                print("Not a valid input...")
    else:
        # after signing up, user will get customer role
        role = "customer"

    # dictionary in the dictionary, where the username is the key of the external dictionary,
    # and user data are the keys to the internal
    users_dict[username] = {
        'password': password,
        'first_name': first_name,
        'last_name': last_name,
        'role': role
    }

    if current_user_role[0] == 'manager':
        print("The new employee is hired.\n")
    else:
        print("You are successfully registered.\n")
        current_user_role.clear()
        current_username.append(username)
        current_user_role.append(role)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~ SIGN OUT ~~~~~~~~~~~~~~~~~~~~~~~~~
def sign_out(users_dict, current_username, current_user_role):
    print("\nSigned out successfully.\n")
    current_username.clear()
    current_user_role.clear()
    current_user_role.append('unregistered')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~ LOG IN ~~~~~~~~~~~~~~~~~~~~~~~~~~
def log_in(users_dict, current_username, current_user_role):
    # entering the valid username
    while True:
        username = input("\nEnter your username: ")
        if username in users_dict.keys():
            break
        else:
            print("Username that you have entered is non-existent.\n")

    # entering the valid password
    while True:
        password = input("Enter your password: ")
        if password == users_dict[username]['password']:
            print("\nYou are successfully logged in.\n")
            break
        else:
            print("\nYour password is incorrect.")

    current_user_role.clear()
    current_username.clear()
    current_username.append(username)
    current_user_role.append(users_dict[username]['role'])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~ CHANGE DATA ~~~~~~~~~~~~~~~~~~~~~~~~
def change_data(users_dict, current_username, current_user_role):
    messages.change_data_message()
    username = current_username[0]

    # input checks
    while True:
        answer = input("> ")

        # name changing
        if answer == '1':
            while True:
                first_name = input("Set your desirable name: ")
                if first_name == '\n' or len(first_name) == 0 or first_name.isspace():
                    print("Wrong input.\n")
                else:
                    users_dict[username]['first_name'] = first_name
                    print(f"You have changed your name to {first_name}.\n")
                    return

        # surname changing
        elif answer == '2':
            while True:
                last_name = input("Set your desirable surname: ")
                if last_name == '\n' or len(last_name) == 0 or last_name.isspace():
                    print("Wrong input.\n")
                else:
                    users_dict[username]['last_name'] = last_name
                    print(f"You have changed your surname to {last_name}.\n")
                    return

        # password changing
        elif answer == '3':
            while True:
                users_dict[username]['password'] = input("Set your desirable password: ")
                if has_numbers(users_dict[username]['password']) and len(users_dict[username]['password']) >= 6:
                    print(f"You have changed your password to {users_dict[username]['password']}.\n")
                    return
                else:
                    print("Password must contain a number, and must be 6+ characters long!\n")
        # wrong input
        else:
            print("Incorrect input.")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~ SEARCH USERS ~~~~~~~~~~~~~~~~~~~~~~~
def enter_name_or_surname(answer):
    while True:
        if answer == '2':
            data = input("Enter customer's first name: ")
        else:
            data = input("Enter customer's last name: ")

        if data == '\n' or len(data) == 0 or data.isspace():
            print("Wrong input.\n")
        else:
            return data

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# checking whether the string that was passed has any numbers in it
def has_numbers(string):
    return any(char.isdigit() for char in string)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
