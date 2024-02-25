from tabulate import tabulate
import messages
import serialization
import datetime

terms = {}
movies = {}
projections = {}
serialization.load_terms(terms)
serialization.load_movies(movies)
serialization.load_projections(projections)
serialization.save_terms(terms)


def list_of_movies():
    with open("text_files/movies.txt", encoding='utf8') as file:
        file_lines = file.readlines()
        movies_list = []
        for line in file_lines:
            line = line.strip().replace('\n', '').split('/')
            movies_list.append(line)
    col_names = ['INDEX', 'MOVIE NAME', 'GENRE', 'DURATION', 'DIRECTORS', 'CAST', 'COUNTRY', 'YEAR']
    print(tabulate(movies_list, headers=col_names, tablefmt='fancy_grid'))


# ------------------- SEARCH MOVIES -------------------

input_dict = {
    '1': 'name',
    '2': 'genre',
    '3': 'duration',
    '4': 'directors',
    '5': 'cast',
    '6': 'country',
    '7': 'year'
}
duration_dict = {
    '1': 'min duration',
    '2': 'max duration',
    '3': 'exact duration',
    '4': 'set boundaries',
    '7': 'year'
}


def search_movies():
    return_value = []   # if there is nothing in this list, return will bring us to the main again
    resulting_movies_indexes = []
    for index in movies.keys():      # for beginning, all movies will be added to the list;
        resulting_movies_indexes.append(index)       # later on some of them will be removed due to specified criteria
    while True:
        messages.movie_search_message()
        answer = input("> ")

        # checks for duration
        if answer == '3':
            while True:
                messages.duration_message()
                answer = input("> ")
                if answer in duration_dict.keys():
                    criteria = duration_dict[answer]
                    input_criteria_value(criteria, resulting_movies_indexes, return_value)
                    if return_value == [1]:
                        break
                    elif len(return_value) == 0:
                        return  # returning to the main
                else:
                    print("Wrong input...")

        # checks for other criteria
        elif answer in input_dict.keys():
            criteria = input_dict[answer]
            input_criteria_value(criteria, resulting_movies_indexes, return_value)
            if len(return_value) == 0:
                return  # returning to the main
        else:
            print("Wrong input...")


# example: criteria = genre -> criteria_value = drama
def input_criteria_value(criteria, resulting_movies_indexes, return_value):
    current_resulting_indexes = []
    if criteria == 'set boundaries':
        while True:
            criteria_value = input("Enter two values separated by space: ").split()
            if len(criteria_value) == 2:
                counter = 0
                for num in criteria_value:
                    if not num.isdigit():
                        print("You must type in a number...")
                    else:
                        counter += 1
                if counter == 2:
                    break
            else:
                print("You must enter two numbers!")
    elif criteria in duration_dict.values():
        while True:
            criteria_value = input(f"Enter the {criteria} of the movie: ")
            if criteria_value.isdigit():
                break
            else:
                print("You must enter a number!\n")
    else:
        criteria_value = input(f"Enter the {criteria} of the movie: ")

    for index in resulting_movies_indexes:
        if criteria == 'min duration':
            if criteria_value < movies[index]['duration']:
                current_resulting_indexes.append(index)
        elif criteria == 'max duration':
            if criteria_value > movies[index]['duration']:
                current_resulting_indexes.append(index)
        elif criteria == 'exact duration':
            if criteria_value in movies[index]['duration']:
                current_resulting_indexes.append(index)
        elif criteria == 'set boundaries':
            if (criteria_value[0] < movies[index]['duration']) and (criteria_value[1] > movies[index]['duration']):
                current_resulting_indexes.append(index)

        elif criteria_value.lower() in movies[index][criteria].lower():
            current_resulting_indexes.append(index)

    resulting_movies_indexes.clear()             # only movies that met specified criteria will be added to the list
    for i in current_resulting_indexes:
        resulting_movies_indexes.append(i)

    other_criteria_input(resulting_movies_indexes, return_value)


# checking whether user wants to enter another criteria
def other_criteria_input(resulting_movies_indexes, return_value):
    print("Do you want to enter any other criteria: Y/N")
    while True:
        yes_no = input("> ")
        if yes_no.lower() == 'y':
            return_value.append(1)
            return
        elif yes_no.lower() == 'n':
            print_results(resulting_movies_indexes, return_value)
            return
        else:
            print("Wrong input...")


def print_results(resulting_movies_indexes, return_value):
    resulting_movies_list = []
    for index in resulting_movies_indexes:
        resulted_movies = list(movies[index].values())
        resulting_movies_list.append(resulted_movies)
    col_names = ['MOVIE NAME', 'GENRE', 'DURATION', 'DIRECTORS', 'CAST', 'COUNTRY', 'YEAR']
    if len(resulting_movies_list) == 0:
        print("\nWe couldn't find anything to match your search...")
    else:
        print(tabulate(resulting_movies_list, headers=col_names, tablefmt='fancy_grid', showindex='always'))
    return_value.clear()

# ------------------------------------------------------


# ------------------------------------------------------
def search_projection_terms():
    resulting_list = []
    while True:
        messages.projection_terms()
        answer = input("> ")
        if answer in projections_input_dict.keys():
            projections_input_dict[answer](resulting_list)
            break
        else:
            print("Wrong input...\n")

    print_projection_terms(resulting_list)
    return


def enter_movie_name(resulting_list):
    while True:
        name_input = input("Enter the name of the projection: ")
        for key in terms.keys():
            projection_key = key[:4]
            projection = projections[projection_key]['name']
            if name_input.lower() in projection.lower():
                resulting_list.append(key)
        return


def enter_hall(resulting_list):
    while True:
        print("These are the available halls: A1, B1")
        hall_input = input("Enter the hall: ")
        for key in terms.keys():
            projection_key = key[:4]
            projection = projections[projection_key]['hall']
            if hall_input.lower() in projection.lower():
                resulting_list.append(key)
        return


def enter_date(resulting_list):
    date_format = '%d-%m-%Y'
    while True:
        valid = True
        date_input = input("\nEnter the valid date of the projection: DD-MM-YYYY\n> ")
        try:
            bool(datetime.datetime.strptime(date_input, date_format))
        except ValueError:
            valid = False
        if valid:     # valid will be true if user entered a valid date
            for key in terms.keys():
                if date_input in terms[key]['date']:
                    resulting_list.append(key)
            return


def enter_beginning(resulting_list):
    while True:
        try:
            beginning_input = input(f"\nEnter the beginning of the projection: XX:XX\n> ")
            check_if_valid = beginning_input.split(':')
            if (24 >= int(check_if_valid[0]) >= 0) and (60 > int(check_if_valid[1]) >= 0) and len(check_if_valid) == 2:
                for key in terms.keys():
                    projection_key = key[:4]
                    projection = projections[projection_key]['beginning']
                    if beginning_input in projection:
                        resulting_list.append(key)
                return
            else:
                print("You must enter a valid time!\n")

        except ValueError:
            print("Incorrect input...\n")
        except IndexError:
            print("Incorrect input...\n")


def enter_ending(resulting_list):
    while True:
        try:
            ending_input = input(f"\nEnter the ending of the projection: XX:XX\n> ")
            check_if_valid = ending_input.split(':')
            if (24 >= int(check_if_valid[0]) >= 0) and (60 > int(check_if_valid[1]) >= 0) and len(check_if_valid) == 2:
                for key in terms.keys():
                    projection_key = key[:4]
                    projection = projections[projection_key]['ending']
                    if ending_input in projection:
                        resulting_list.append(key)
                return
            else:
                print("You must enter a valid time!\n")

        except ValueError:
            print("Incorrect input...\n")
        except IndexError:
            print("Incorrect input...\n")


def enter_term(current_user_role, reserve_ticket=False):
    # reserve_ticket will be True if this function was called within ticket_reservation() in ticket_function.py,
    # and it is used for blocking the attempt to reserve a ticket on expired term
    while True:
        counter = 0
        term_code = input("\nEnter the code of term: ")
        for key in terms.keys():
            if term_code == key:
                counter += 1
                break
        else:
            print("There is no such term...\n")
        if counter > 0:
            break

    # checking whether projection term has expired
    if terms[term_code]['state'] == 'expired' and (current_user_role[0] == 'customer' or reserve_ticket):
        return 'expired'
    else:
        return term_code


def print_projection_terms(resulting_list):    # the resulted list is a list containing the codes of projections
    results = []        # list that will be printed
    resulting_terms = []
    for index in resulting_list:
        key = projections[index[:4]]
        resulting_terms.append(key['name'])
        resulting_terms.append(key['hall'])
        resulting_terms.append(terms[index]['date'])
        resulting_terms.append(key['beginning'])
        resulting_terms.append(key['ending'])
        resulting_terms.append(index)

        results.append(list(resulting_terms))
        resulting_terms.clear()
    if len(results) == 0:
        print("\nWe couldn't find anything to match your search...")
    else:
        col_names = ['NAME', 'HALL', 'DATE', 'BEGINNING', 'ENDING', 'TERM CODES']
        print(tabulate(results, headers=col_names, tablefmt='fancy_grid', showindex='always'))


projections_input_dict = {
    '1': enter_movie_name,
    '2': enter_hall,
    '3': enter_date,
    '4': enter_beginning,
    '5': enter_ending
}
