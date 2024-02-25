import datetime


def save_tickets(tickets):
    with open("text_files/tickets.txt", 'w', encoding='utf8') as file:
        for index in tickets.keys():
            key = tickets[index]
            username = key['username']
            name_and_surname = key['name_and_surname']
            sellers_data = key['sellers_data']
            term_code = key['term_code']
            seat = key['seat']
            date = key['date']
            price = key['price']
            state = key['state']

            file.write(f"{index}/{username}/{name_and_surname}/{sellers_data}/{term_code}/{seat}/{date}/{price}/{state}\n")


def load_tickets(tickets):
    with open("text_files/tickets.txt", encoding='utf8') as file:
        file_lines = file.readlines()
        for line in file_lines:
            line = line.strip().replace('\n', '').split('/')
            tickets[line[0]] = {
                'username': line[1],
                'name_and_surname': line[2],
                'sellers_data': line[3],
                'term_code': line[4],
                'seat': line[5],
                'date': line[6],
                'price': line[7],
                'state': line[8]
            }
        # upon exiting for loop, line[0] will be the index of last ticket, and it is returned for ticket index generator
        return line[0]


def load_halls(halls):
    with open("text_files/halls.txt", encoding='utf8') as file:
        file_lines = file.readlines()
        for line in file_lines:
            line = line.strip().replace('\n', '').split('/')
            halls[line[0]] = {
                'hall_name': line[1],
                'rows_number': line[2],
                'columns': line[3]
            }


def load_terms(terms):
    with open("text_files/terms.txt", encoding='utf8') as file:
        file_lines = file.readlines()
        for line in file_lines:
            line = line.strip().replace('\n', '').split('/')
            terms[line[0]] = {
                'date': line[1],
                'state': line[2]
            }


def save_terms(terms):
    with open("text_files/terms.txt", 'w', encoding='utf8') as file:
        today = datetime.date.today().strftime("%d-%m-%Y")
        today = today.split('-')
        for term_code in terms.keys():
            date = terms[term_code]['date']
            check_date = terms[term_code]['date'].split('-')

            # checking whether projection term has expired
            if int(today[2]) > int(check_date[2]):
                state = 'expired'
            elif int(today[1]) > int(check_date[1]):
                state = 'expired'
            elif int(today[0]) > int(check_date[0]):
                state = 'expired'
            else:
                state = terms[term_code]['state']

            file.write(f"{term_code}/{date}/{state}\n")


def load_projections(projections):
    with open("text_files/projections.txt", encoding='utf8') as file:
        file_lines = file.readlines()
        for line in file_lines:
            line = line.strip().replace('\n', '').split('/')
            projections[line[0]] = {
                'hall': line[1],
                'beginning': line[2],
                'ending': line[3],
                'days': line[4],
                'name': line[5],
                'cost': line[6]
            }


def load_movies(movies):
    with open("text_files/movies.txt", encoding='utf8') as file:
        file_lines = file.readlines()
        for line in file_lines:
            line = line.strip().replace('\n', '').split('/')
            movies[line[0]] = {     # movie index
                'name': line[1],
                'genre': line[2],
                'duration': line[3],
                'directors': line[4],
                'cast': line[5],
                'country': line[6],
                'year': line[7]
            }


def load_users(users_dict):
    with open("text_files/users.txt", encoding="utf8") as file:
        file_lines = file.readlines()
        for line in file_lines:
            # deletes spaces if there are any, turns the whole line into a list
            line = line.strip().replace("\n", "").split('/')
            users_dict[line[0]] = {
                'password': line[1],
                'first_name': line[2],
                'last_name': line[3],
                'role': line[4]
            }


def save_users(users_dict, current_user_role, current_username):
    with open("text_files/users.txt", 'w', encoding='utf8') as file:
        for username in users_dict.keys():
            user_data = users_dict[username]
            password = user_data['password']
            first_name = user_data['first_name']
            last_name = user_data['last_name']
            role = user_data['role']

            file.write(f"{username}/{password}/{first_name}/{last_name}/{role}\n")
        print("\nExiting the app...")
        exit()
