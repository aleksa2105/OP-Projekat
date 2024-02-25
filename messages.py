def entry_message():
    print("""
        -------------------------------------------
         ~Welcome to the Bosnian edition of Cinema~
        -------------------------------------------""")


# TODO organize messages in categories

# ~~~~~~~~~~~~~~~~~~ TICKET_FUNCTIONS_MESSAGES ~~~~~~~~~~~~~~~~~~~~
def ticket_reservation_message():
    print("""
Options:
(1) SEARCH TERMS
(2) ENTER THE CODE OF TERM
(X) RETURN
    """)

def search_tickets_message():
    print("""
Search by:
(1) TERM CODE
(2) CUSTOMER'S NAME
(3) CUSTOMER'S SURNAME
(4) TICKET'S DATE
(5) PROJECTION BEGINNING
(6) PROJECTION ENDING
(7) RESERVED/SOLD TICKET
(X) RETURN
    """)

def choose_user_reservation():
    print("\nTo reserve a ticket please choose something from available options: ")
    print("(1) UNREGISTERED CUSTOMER")
    print("(2) REGISTERED CUSTOMER\n")

def change_ticket():
    print("\n(1) CHANGE PROJECTION TERM")
    print("(2) CHANGE NAME AND SURNAME")
    print("(3) CHANGE SEAT")
    print("(X) RETURN")

# ~~~~~~~~~~~~~~~~~~~ MOVIE_FUNCTIONS_MESSAGES ~~~~~~~~~~~~~~~~~~~~
def reports_message():
    print("""
Options:
(a) List for the selected date of sale    
(b) List for the selected date of the cinema screening   
(c) List for the selected date of sale and the selected seller
(d) Total number and price of sold tickets for the selected day of sale
(e) Total number and price of tickets sold for the selected day of the screening
(f) The total price of tickets sold for a given film in all screenings
(g) Total number and total price of tickets sold for the selected day of sale and the selected seller
(h) Total number and total price of sold tickets by sellers (for each seller)
    in the last 30 days   
    """)
def projection_terms():
    print("""
Available options:
(1) MOVIE NAME
(2) HALL
(3) DATE
(4) BEGINNING
(5) ENDING
    """)

def movie_search_message():
    print(""" 
Available criteria:
(1) MOVIE NAME     
(2) GENRE          
(3) DURATION       
(4) DIRECTORS       
(5) CAST
(6) COUNTRY
(7) YEAR
    """)

def duration_message():
    print("""
~ in minutes ~
(1) MIN DURATION
(2) MAX DURATION
(3) EXACT DURATION
(4) SET BOUNDARIES
    """)

# ~~~~~~~~~~~~~~~~~~~~~~~~~ MAIN MESSAGES ~~~~~~~~~~~~~~~~~~~~~~~~
def unregistered():
    print("""
Options:
(q) SIGN UP    (1) LIST OF MOVIES
(w) LOG IN     (2) SEARCH MOVIES
(e) EXIT       (3) PROJECTION TERMS
    """)

def customer():
    print("""
Options:
(q) SIGN OUT       (1) LIST OF MOVIES      (4) RESERVE TICKET   
(w) MANAGE DATA    (2) SEARCH MOVIES       (5) OVERVIEW OF RESERVED TICKETS
(e) EXIT           (3) PROJECTION TERMS    (6) CANCEL RESERVED TICKETS
    """)

def seller():
    print("""
Options:
(q) SIGN OUT            
(w) MANAGE DATA    
(e) EXIT           
(1) LIST OF MOVIES      
(2) SEARCH MOVIES       
(3) PROJECTION TERMS    
(4) TICKET RESERVATION          
(5) OVERVIEW OF RESERVED TICKETS
(6) CANCEL TICKETS                
(7) SEARCH TICKETS
(8) DIRECT TICKET SALE
(9) SELL RESERVED TICKETS    
(10) CHANGE TICKET INFORMATION          
(11) AUTOMATIC RESERVATION CANCELLATION         
    """)

def manager():
    print("""
Options:
(q) SIGN OUT       (1) LIST OF MOVIES             
(w) CHANGE DATA    (2) SEARCH MOVIES      
(e) EXIT           (3) PROJECTION TERMS    
(r) NEW STAFF      (4) REPORTS   
    """)

# ~~~~~~~~~~~~~~~~~~~~ USER_FUCNTIONS_MESSAGES ~~~~~~~~~~~~~~~~~~~~~
def change_data_message():
    print("""
(1) CHANGE FIRST NAME
(2) CHANGE SURNAME 
(3) CHANGE PASSWORD
    """)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ REPORTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def report_d():
    print("""
(1) Monday
(2) Tuesday
(3) Wednesday
(4) Thursday
(5) Friday
(6) Saturday
(7) Sunday
    """)
