import messages
import datetime
import ticket_functions
import movie_functions
from tabulate import tabulate

tickets = ticket_functions.tickets
terms = movie_functions.terms
projections = movie_functions.projections


# ~~~~~~~~~~~~~~~~~~~~~~~~~ REPORTS ~~~~~~~~~~~~~~~~~~~~~~~~~~
days_dict = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7
}


def reports(users_dict, current_username, current_user_role):
    messages.reports_message()

    while True:
        results = []
        answer = input("> ")

        if answer == 'a':
            report_a()
            break

        elif answer == 'b':
            report_b()
            break

        elif answer == 'c':
            report_c()
            break

        elif answer == 'd':
            report_d()
            break

        elif answer == 'e':
            report_e()
            break

        elif answer == 'g':
            report_g()
            break

        elif answer == 'f':
            report_f()
            break

        elif answer == 'h':
            report_h()
            break

        else:
            print("\nWrong input...\n")


def report_a():
    date = ticket_functions.enter_date(results=[])
    print_tickets = []

    for index in tickets.keys():
        if date == tickets[index]['date'] and tickets[index]['state'] == 'sold':
            print_tickets.append(list(tickets[index].values()))

    print_reports(print_tickets)


def report_b():
    date = ticket_functions.enter_date(results=[])
    print_tickets = []
    ticket_term_codes = []

    for term_code in terms.keys():
        if date == terms[term_code]['date']:
            ticket_term_codes.append(term_code)

    for index in tickets.keys():
        for term_code in ticket_term_codes:
            if term_code == tickets[index]['term_code'] and tickets[index]['state'] == 'sold':
                print_tickets.append(list(tickets[index].values()))

    print_reports(print_tickets)


def report_c(print_results=True):
    date = ticket_functions.enter_date(results=[])
    sellers_data = input("Enter sellers name and surname separated by space: ").lower()
    print_tickets = []
    total_price = 0

    for index in tickets.keys():
        key = tickets[index]
        if date == key['date'] and key['state'] == 'sold' and sellers_data in key['sellers_data'].lower():
            print_tickets.append(list(tickets[index].values()))
            total_price += int(tickets[index]['price'])

    total_num = len(print_tickets)

    if print_results:
        print_reports(print_tickets)
    else:
        return total_num, total_price


def report_d():

    while True:
        messages.report_d()
        answer = input("\n> ")

        if answer in days_dict.keys():
            selected_day = days_dict[answer]
            break
        else:
            print("\nWrong input.\n")

    total_num = 0
    total_price = 0
    for index in tickets.keys():
        ticket_date = tickets[index]['date']
        day = datetime.datetime.strptime(ticket_date, "%d-%m-%Y").isoweekday()
        if selected_day == day:
            total_num += 1
            total_price += int(tickets[index]['price'])

    print_results = [[total_num, total_price]]
    if total_num > 0:
        col_names = ['TOTAL NUMBER', 'TOTAL PRICE']
        print(tabulate(print_results, headers=col_names, tablefmt='fancy_grid'))
    else:
        print("\nWe couldn't find anything to match your search...\n")


def report_e():
    while True:
        messages.report_d()
        answer = input("\n> ")

        if answer in days_dict.keys():
            selected_day = days_dict[answer]
            break
        else:
            print("\nWrong input.\n")

    total_num = 0
    total_price = 0
    for index in tickets.keys():
        term_code = tickets[index]['term_code']
        projection_key = term_code[:4]

        if str(selected_day) in projections[projection_key]['days']:
            total_num += 1
            total_price += int(tickets[index]['price'])

    print_results = [[total_num, total_price]]
    if total_num > 0:
        col_names = ['TOTAL NUMBER', 'TOTAL PRICE']
        print(tabulate(print_results, headers=col_names, tablefmt='fancy_grid'))
    else:
        print("\nWe couldn't find anything to match your search...\n")


def report_f():
    movie_name = input("\nEnter the name of the movie: ")
    total_price = 0

    for index in tickets.keys():
        term_code = tickets[index]['term_code']
        projection_key = term_code[:4]
        if projections[projection_key]['name'].lower() == movie_name.lower():
            total_price += int(tickets[index]['price'])

    print_results = [[str(total_price)]]

    if total_price == 0:
        print(f"\nThere are no tickets for {movie_name.capitalize()}.\n")
    else:
        col_names = ['TOTAL PRICE']
        print(tabulate(print_results, headers=col_names, tablefmt='fancy_grid'))


def report_g():
    while True:
        messages.report_d()
        answer = input("\n> ")

        if answer in days_dict.keys():
            selected_day = days_dict[answer]
            break
        else:
            print("\nWrong input.\n")

    sellers_data = input("Enter sellers name and surname separated by space: ").lower()

    total_num = 0
    total_price = 0
    for index in tickets.keys():
        ticket_date = tickets[index]['date']
        day = datetime.datetime.strptime(ticket_date, "%d-%m-%Y").isoweekday()
        if selected_day == day and tickets[index]['sellers_data'] == sellers_data:
            total_num += 1
            total_price += int(tickets[index]['price'])

    print_results = [[str(total_num), str(total_price)]]

    if total_num == 0:
        print("\nWe couldn't find anything to match your search.\n")
    else:
        col_names = ['TOTAL NUMBER', 'TOTAL PRICE']
        print(tabulate(print_results, headers=col_names, tablefmt='fancy_grid'))


def report_h():
    last_30_days = datetime.datetime.now() - datetime.timedelta(days=30)

    sellers = {}
    for index in tickets.keys():
        if tickets[index]['state'] == 'sold':
            seller = tickets[index]['sellers_data']
            sellers[seller] = {
                'total_num': 0,
                'total_price': 0
            }

    for index in tickets.keys():
        if tickets[index]['state'] == 'sold':
            ticket_date = tickets[index]['date']
            date = datetime.datetime.strptime(ticket_date, "%d-%m-%Y")
            seller = tickets[index]['sellers_data']
            if date >= last_30_days:
                sellers[seller]['total_num'] += 1
                sellers[seller]['total_price'] += int(tickets[index]['price'])

    print_results = []
    for seller in sellers.keys():
        list_of_sellers = [seller, sellers[seller]['total_num'], sellers[seller]['total_price']]
        print_results.append(list(list_of_sellers))

    col_names = ['SELLER', 'TOTAL NUMBER', 'TOTAL PRICE']
    print(tabulate(print_results, headers=col_names, tablefmt='fancy_grid'))


def print_reports(print_tickets):

    if len(print_tickets) == 0:
        print("\nWe couldn't find anything to match your search.\n")
    else:
        col_names = ['USERNAME', 'NAME & SURNAME', 'SELLER', 'TERM CODE', 'SEAT', 'DATE', 'PRICE', 'STATE']
        print(tabulate(print_tickets, headers=col_names, tablefmt='fancy_grid', showindex='always'))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
