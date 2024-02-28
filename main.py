import movie_functions
import ticket_functions
import user_functions
import serialization
import messages
import reports

users_dict = {}
current_username = []
current_user_role = ['unregistered']

serialization.load_users(users_dict)
messages.entry_message()

if __name__ == '__main__':
    while True:

        messages_dict = {
            'unregistered': messages.unregistered,
            'customer': messages.customer,
            'seller': messages.seller,
            'manager': messages.manager
        }
        movie_dict = {
            '1': movie_functions.list_of_movies,
            '2': movie_functions.search_movies,
            '3': movie_functions.search_projection_terms
        }
        unregistered_dict = {
            'q': user_functions.sign_up,
            'w': user_functions.log_in,
            'e': serialization.save_users
        }
        customer_dict = {
            'q': user_functions.sign_out,
            'w': user_functions.change_data,
            'e': serialization.save_users,
            '4': ticket_functions.ticket_reservation,
            '5': ticket_functions.tickets_overview,
            '6': ticket_functions.cancel_reserved_ticket
        }
        manager_dict = {
            'q': user_functions.sign_out,
            'w': user_functions.change_data,
            'e': serialization.save_users,
            'r': user_functions.sign_up,
            '4': reports.reports

        }
        seller_dict = {
            'q': user_functions.sign_out,
            'w': user_functions.change_data,
            'e': serialization.save_users,
            '4': ticket_functions.ticket_reservation,
            '5': ticket_functions.tickets_overview,
            '6': ticket_functions.cancel_reserved_ticket,
            '7': ticket_functions.search_tickets,
            '8': ticket_functions.direct_ticket_sale,
            '9': ticket_functions.sell_reserved_ticket,
            '10': ticket_functions.change_ticket,
            '11': ticket_functions.automatic_reservation_cancellation
        }

        messages_dict[current_user_role[0]]()

        answer = input("> ").lower()

        # inputs for movies
        if answer in movie_dict.keys():
            movie_dict[answer]()

        # inputs for unregistered
        elif (answer in unregistered_dict.keys()) and (current_user_role[0] == 'unregistered'):
            unregistered_dict[answer](users_dict, current_username, current_user_role)

        # inputs for customer
        elif (answer in customer_dict.keys()) and (current_user_role[0] == 'customer'):
            customer_dict[answer](users_dict, current_username, current_user_role)

        # inputs for manager
        elif (answer in manager_dict.keys()) and (current_user_role[0] == 'manager'):
            manager_dict[answer](users_dict, current_username, current_user_role)

        # inputs for seller
        elif (answer in seller_dict.keys()) and (current_user_role[0] == 'seller'):
            seller_dict[answer](users_dict, current_username, current_user_role)

        else:
            print("Wrong input...")
