import messages
import datetime
import movie_functions
import serialization
from tabulate import tabulate

import user_functions

halls = {}
tickets = {}
last_ticket_index = int(serialization.load_tickets(tickets))
serialization.load_halls(halls)
terms = movie_functions.terms
projections = movie_functions.projections
today = datetime.date.today().strftime("%d-%m-%Y")


# ~~~~~~~~~~~~~~~~~~~~ TICKET RESERVATION ~~~~~~~~~~~~~~~~~~~~
def ticket_reservation(users_dict, current_username, current_user_role, direct_sale=False):
    while True:
        global today
        username = []   # username that will be added to ticket info
        name_and_surname = []   # name & surname that will be added to ticket info
        while True:
            messages.ticket_reservation_message()
            answer = input("> ")

            # search projection terms
            if answer == '1':
                movie_functions.search_projection_terms()

            # enter projection term code
            elif answer == '2':
                expired_check = movie_functions.enter_term(current_user_role, reserve_ticket=True)
                if expired_check == 'expired':
                    print("\nThe projection term has expired.")
                else:
                    term_code = expired_check
                    # seller needs to enter specific user for ticket reservation
                    if current_user_role[0] == 'seller':
                        choose_user(users_dict, username, name_and_surname)

                    seat = choose_seat(term_code)
                    break

            elif answer.lower() == 'x':
                return
            # wrong input
            else:
                print("Wrong input...")

        # saving new ticket
        index = next(tickets_index_generator())
        save_seat = seat[0] + seat[1]

        if current_user_role[0] == 'customer':
            first_name = users_dict[current_username[0]]['first_name']
            last_name = users_dict[current_username[0]]['last_name']
            username.append(current_username[0])
            name_and_surname.append(first_name + ' ' + last_name)
            state = 'reserved'
            sellers_data = ''

        elif direct_sale:
            state = 'sold'
            sellers_data = users_dict[current_username[0]]['first_name'] + ' ' + users_dict[current_username[0]]['last_name']
        else:
            state = 'reserved'
            sellers_data = ''

        # Loyalty card discounts for given customer
        user_spending = 0
        last_year_date = datetime.datetime.now() - datetime.timedelta(days=365)
        for i in tickets.keys():
            ticket_date = tickets[i]['date']
            ticket_date = datetime.datetime.strptime(ticket_date, "%d-%m-%Y")
            if ticket_date >= last_year_date:
                if len(username[0]) > 0 and tickets[i]['username'] == username[0]:
                    user_spending += float(tickets[i]['price'])

        # Tuesday, Weekdays discounts
        if datetime.datetime.strptime(today, "%d-%m-%Y").isoweekday() == 2:
            price = int(projections[term_code[:4]]['cost']) - 50
        elif datetime.datetime.strptime(today, "%d-%m-%Y").isoweekday() in [6, 7]:
            price = int(projections[term_code[:4]]['cost']) + 50
        else:
            price = projections[term_code[:4]]['cost']

        if user_spending > 5000:
            price *= 0.9
            price = int(price)

        tickets[index] = {
            'username': username[0],
            'name_and_surname': name_and_surname[0],
            'sellers_data': sellers_data,
            'term_code': term_code,
            'seat': save_seat,
            'date': today,
            'price': price,
            'state': state
        }

        print("Successfully reserved.\n")
        serialization.save_tickets(tickets)

        if direct_sale:
            print("Do you want to sell another ticket: Y/N")
        else:
            print("Do you want to reserve another ticket: Y/N")
        return_val = enter_another_one()
        if not return_val:
            return


def choose_user(users_dict, username, name_and_surname):    # Option for seller
    while True:
        messages.choose_user_reservation()
        answer = input("> ")

        # entering the first and last name for unregistered person
        if answer == '1':
            print("Please enter the following.\n")
            # entering the first name
            while True:
                first_name = input("First name: ").strip()
                if first_name == '\n' or len(first_name) == 0 or first_name.isspace():
                    print("Wrong input.\n")
                else:
                    break

            # entering the last name
            while True:
                last_name = input("Last name: ").strip()
                if last_name == '\n' or len(last_name) == 0 or last_name.isspace():
                    print("Wrong input.\n")
                else:
                    break

            name_and_surname.append(first_name.strip() + " " + last_name.strip())
            username.append('')
            return

        # entering username for registered person
        elif answer == '2':
            while True:
                person = input("Please enter person's username:\n> ")
                counter = 0
                for user in users_dict.keys():
                    # person must be signed in by this username and must be a customer
                    if person == user and users_dict[user]['role'] == 'customer':
                        counter += 1
                        break
                else:
                    print("The username that you have entered is not valid.\n")

                if counter > 0:
                    username.append(person)
                    name_and_surname.append(users_dict[person]['first_name'] + ' ' + users_dict[person]['last_name'])
                    return


def choose_seat(term_code):
    seat = []       # seat that will be returned
    used_seats = []
    projection_key = term_code[:4]
    current_hall = projections[projection_key]['hall']      # hall that is used for entered term

    # getting used seats for that exact term
    for index in tickets.keys():
        if term_code == tickets[index]['term_code']:
            used_seats.append(tickets[index]['seat'])

    # printing out empty seats
    for row in range(int(halls[current_hall]['rows_number'])):
        column_list = halls[current_hall]['columns'].split(",")     # list of all columns [ A, B, C, D, E, F ]
        column_str = ''     # this string will be modified and printed later on
        column_index = 0
        for column in column_list:
            for used_seat in used_seats:
                if int(used_seat[0]) == row and used_seat[1] == column:
                    column_list[column_index] = 'X'
            column_str = str(column_str + column_list[column_index] + ' ')
            column_index += 1
        print(f"\nRow {row}: {str(column_str)}")

    # prompting user for seat
    while True:
        try:
            enter_seat = input("\nEnter the desired seat: (e.g. 0A)\n> ")
            wanted_row = int(enter_seat[0])
            wanted_column = enter_seat[1:].upper()

            # checking if seat is valid
            if not ((0 <= wanted_row < int(halls[current_hall]['rows_number'])) and wanted_column in 'ABCDEF' and len(wanted_column) == 1):
                print("The seat that you have entered is not valid.\n")
            else:
                # checking if seat is already taken
                counter = 0
                for used_seat in used_seats:
                    if wanted_row == int(used_seat[0]) and wanted_column == used_seat[1].upper():
                        print("Seat is already in use.\n")
                        counter += 1
                if counter == 0:
                    seat.append(str(wanted_row))
                    seat.append(wanted_column)
                    break

        except ValueError:
            print("Incorrect input...\n")
        except IndexError:
            print("Incorrect input...\n")

    return seat

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~ TICKET OVERVIEW ~~~~~~~~~~~~~~~~~~~~~~
def tickets_overview(users_dict, current_username, current_user_role, print_results=True):
    results = []
    resulting_list = []
    for index in tickets.keys():
        key = tickets[index]
        projection_key = key['term_code'][:4]
        projection = projections[projection_key]

        name_and_surname = key['name_and_surname'].split()
        first_name = name_and_surname[0].capitalize()
        last_name = name_and_surname[1].capitalize()

        # printing all tickets, since seller is calling this function
        if current_user_role[0] == 'seller':
            resulting_list.append(key['term_code'])
            resulting_list.append(key['seat'])
            resulting_list.append(first_name)
            resulting_list.append(last_name)
            resulting_list.append(projection['name'])
            resulting_list.append(key['date'])
            resulting_list.append(projection['beginning'])
            resulting_list.append(projection['ending'])
            resulting_list.append(key['state'])

            results.append(list(resulting_list))
            resulting_list.clear()

        # printing only reservations for customer that is signed in
        elif current_username[0] == key['username'] and key['state'] == 'reserved' and current_user_role[0] == 'customer':
            resulting_list.append(key['term_code'])
            resulting_list.append(key['seat'])
            resulting_list.append(projection['name'])
            resulting_list.append(key['date'])
            resulting_list.append(projection['beginning'])
            resulting_list.append(projection['ending'])

            results.append(list(resulting_list))
            resulting_list.clear()

    if current_user_role[0] == 'seller':
        col_names = ['TERM CODES', 'SEAT', 'FIRST NAME', 'LAST NAME', 'MOVIE NAME',
                     'DATE', 'BEGINNING', 'ENDING', 'STATE']
    else:
        col_names = ['TERM CODES', 'SEAT', 'MOVIE NAME', 'DATE', 'BEGINNING', 'ENDING']

    # if function was called from cancel_tickets(), table won't be printed out
    if print_results:
        print(tabulate(results, headers=col_names, tablefmt='fancy_grid', showindex='always'))
    return results

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~ CANCEL RESERVATION/SELL RESERVED TICKET ~~~~~~~~~~
def cancel_reserved_ticket(users_dict, current_username, current_user_role):
    while True:
        counter = 0
        ticket_index = []
        results = choose_reservations(users_dict, current_username, current_user_role)

        for index in tickets.keys():
            key = tickets[index]
            if results[0] == key['term_code'] and results[1] == key['seat']:
                if current_user_role[0] == 'seller':
                    ticket_index.append(index)
                    counter += 1
                elif current_user_role[0] == 'customer' and key['state'] == 'reserved':
                    ticket_index.append(index)
                    counter += 1

        if counter > 0:
            del tickets[ticket_index[0]]
            serialization.save_tickets(tickets)
            print("Successfully canceled.\n")

            # Asking user if he wants to cancel another reservation
            print("Do you want to cancel another reservation: Y/N")
            return_val = enter_another_one()
            if not return_val:
                return
        else:
            print("\nThat ticket is sold, hence it's not possible to cancel it.\n")


def sell_reserved_ticket(users_dict, current_username, current_user_role):    # Option for seller
    while True:
        counter = 0
        ticket_index = []
        results = choose_reservations(users_dict, current_username, current_user_role)

        for index in tickets.keys():
            key = tickets[index]
            if results[0] == key['term_code'] and results[1] == key['seat'] and key['state'] == 'reserved':
                ticket_index.append(index)
                counter += 1
        if counter > 0:
            break
        else:
            print("\nThat ticket is already sold.\n")

    tickets[ticket_index[0]]['state'] = 'sold'
    sellers_name = users_dict[current_username[0]]['first_name']
    sellers_surname = users_dict[current_username[0]]['last_name']
    tickets[ticket_index[0]]['sellers_data'] = sellers_name + ' ' + sellers_surname

    serialization.save_tickets(tickets)
    print("Successfully sold.\n")


def choose_reservations(users_dict, current_username, current_user_role):
    while True:
        # first we load all reservations
        all_reservations = tickets_overview(users_dict, current_username, current_user_role, print_results=False)
        results = []

        # Entering a valid projection term
        print("\nEnter projection term code:")
        while True:
            term_code = input("> ")
            counter = 0
            for reservation in all_reservations:
                if term_code == reservation[0]:
                    counter += 1
                    results.append(term_code)
                    break
            else:
                print("That projection term isn't valid.\n")
            if counter > 0:
                break

        # Entering a valid seat
        print("\nEnter the seat:")
        while True:
            enter_seat = input("> ").upper()
            counter = 0
            for reservation in all_reservations:
                if term_code == reservation[0] and enter_seat == reservation[1]:
                    counter += 1
                    results.append(enter_seat)
                    break
            else:
                print("That seat isn't valid.\n")
            if counter > 0:
                break

        return results

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~ SEARCH TICKETS ~~~~~~~~~~~~~~~~~~~~~~~
def search_tickets(users_dict, current_username, current_user_role):    # Option for seller
    messages.search_tickets_message()
    results = []
    while True:
        answer = input('> ')

        # search by term
        if answer == '1':
            term_code = movie_functions.enter_term(current_user_role)
            for index in tickets.keys():
                if term_code == tickets[index]['term_code']:
                    results.append(list(tickets[index].values()))
            break

        # search by name/surname
        elif answer == '2' or answer == '3':
            person = user_functions.enter_name_or_surname(answer).lower()

            for index in tickets.keys():
                if person in tickets[index]['name_and_surname'].lower():
                    results.append(list(tickets[index].values()))
            break

        # search by date
        elif answer == '4':
            enter_date(results)
            break

        # search by beginning/ending
        elif answer == '5' or answer == '6':
            all_term_codes = []
            if answer == '5':
                movie_functions.enter_beginning(all_term_codes)
            else:
                movie_functions.enter_ending(all_term_codes)

            for index in tickets.keys():
                for term_code in all_term_codes:
                    if term_code == tickets[index]['term_code']:
                        results.append(list(tickets[index].values()))
            break

        # search for reserved/sold tickets
        elif answer == '7':
            enter_state(results)
            break

        elif answer.lower() == 'x':
            return

        # wrong input
        else:
            print("Wrong input")

    # printing results
    print_searched_tickets(results)
    return


def enter_date(results):
    date_format = '%d-%m-%Y'
    while True:
        valid = True
        date_input = input("Enter the valid date of the projection: DD-MM-YYYY\n> ")
        try:
            bool(datetime.datetime.strptime(date_input, date_format))
        except ValueError:
            valid = False
        if valid:     # valid will be true if user entered a valid date
            for index in tickets.keys():
                if date_input in tickets[index]['date']:
                    results.append(list(tickets[index].values()))
            return date_input


def enter_state(results):
    print("\n(1) RESERVED TICKETS")
    print("(2) SOLD TICKETS")
    while True:
        state = []
        answer = input("> ")
        if answer == '1':
            state.append('reserved')
            break
        elif answer == '2':
            state.append('sold')
            break
        else:
            print("Wrong input.\n")

    for index in tickets.keys():
        if state[0] == tickets[index]['state']:
            results.append(list(tickets[index].values()))
    return


def print_searched_tickets(results):
    if len(results) == 0:
        print("\nWe couldn't find anything to match your search.\n")
        return
    else:
        col_names = ['USERNAME', 'NAME & SURNAME', 'SELLER', 'TERM CODE', 'SEAT', 'DATE', 'PRICE', 'STATE']
        print(tabulate(results, headers=col_names, tablefmt='fancy_grid', showindex='always'))
        results.clear()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~ DIRECT TICKET SALE ~~~~~~~~~~~~~~~~~~~~~
def direct_ticket_sale(users_dict, current_username, current_user_role):
    # since all functions that direct_ticket_sale needs is in ticket reservation
    # we call that function passing it direct_sale parameter,
    # so ticket_reservation can know what state(reserved/sold) to put in ticket information
    ticket_reservation(users_dict, current_username, current_user_role, direct_sale=True)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~ CHANGE TICKET INFORMATION ~~~~~~~~~~~~~~~~~
def change_ticket(users_dict, current_username, current_user_role):

    while True:
        term_code = movie_functions.enter_term(current_user_role)
        name_and_surname = input("Enter name and surname separated by space: ").lower()
        seat = input("Enter the seat: (e.g. 0A)\n> ").lower()
        change_ticket_index = []

        counter = 0
        for index in tickets.keys():
            key = tickets[index]
            if term_code == key['term_code'] and name_and_surname == key['name_and_surname'].lower() and seat == key['seat'].lower():
                counter += 1
                change_ticket_index.append(index)
                break
        if counter > 0:
            break
        else:
            print("\nWe couldn't find anything to match your search...\n")

    while True:
        messages.change_ticket()

        answer = input("\n> ")
        ticket = tickets[change_ticket_index[0]]
        if answer == '1':
            new_term_code = movie_functions.enter_term(current_user_role)
            ticket['term_code'] = new_term_code
            break
        elif answer == '2':
            new_name_and_surname = input("Enter name and surname separated by space: ")
            ticket['name_and_surname'] = new_name_and_surname
            break
        elif answer == '3':
            seat = choose_seat(term_code)
            seat = seat[0] + seat[1]
            ticket['seat'] = seat
            break
        elif answer.lower() == 'x':
            return
        else:
            print("\nWrong input...\n")

    serialization.save_tickets(tickets)
    print("\nChanges have been applied.\n")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~ AUTOMATIC RESERVATION CANCELLATION ~~~~~~~~~~~~
def automatic_reservation_cancellation(users_dict, current_username, current_user_role):

    # getting current time
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    current_time = current_time.split(':')

    tickets_indexes = []  # indexes of tickets that will be canceled

    for index in tickets.keys():
        term_code = tickets[index]['term_code']
        # we only want to cancel tickets that are reserved and expired
        if tickets[index]['state'] == 'sold':
            continue

        projection_code = term_code[:4]
        projection_date = terms[term_code]['date']

        if terms[term_code]['state'] == 'expired':
            tickets_indexes.append(index)
        elif projection_date == today:
            check_time(projection_code, current_time, tickets_indexes, index)

    if len(tickets_indexes) > 0:
        for ticket_index in tickets_indexes:
            del tickets[ticket_index]

        serialization.save_tickets(tickets)
        print("Successfully canceled.\n")
    else:
        print("\nWe could not find any expired reservations.\n")


def check_time(projection_code, current_time, ticket_index, index):
    projection_time = projections[projection_code]['beginning'].split(':')

    projection_minute = int(projection_time[1]) - 30
    projection_hour = int(projection_time[0])

    current_hour = int(current_time[0])
    current_minute = int(current_time[1])

    if projection_minute < 0:
        projection_minute = projection_minute + 60
        projection_hour -= 1

    if current_hour > projection_hour:
        ticket_index.append(index)
        return
    elif current_hour == projection_hour and current_minute > projection_minute:
        ticket_index.append(index)
        return

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def enter_another_one():
    while True:
        yes_no = input("> ")
        if yes_no.lower() == 'y':
            return True
        elif yes_no.lower() == 'n':
            return False
        else:
            print("Wrong input...")


def tickets_index_generator():
    global last_ticket_index
    last_ticket_index += 1
    yield last_ticket_index
