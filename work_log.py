import os
import sys
import datetime
import re

import peewee

db = peewee.SqliteDatabase('entries.db')

FIELDNAMES = ['ID','Name', 'Minutes Spent', 'Date', 'Notes']
DATA_ID_FORMAT = '%Y%m%d%H%M%S%f'

class Entry(peewee.Model):
    #title
    title = peewee.CharField(max_length=255)
    #time spent (in minutes)
    time_spent = peewee.IntegerField(default=0)
    #date that is auto generated at creation
    date = peewee.DateTimeField(default=datetime.datetime.now)
    #optional notes
    notes = peewee.TextField()

    class Meta:
        database = db


def run_program():
    """Create the database if it doesn't already exist"""
    db.connect()
    db.create_tables([Entry], safe=True)

def display_menu():
    clear_screen()
    print("What would you like to do? ")
    choice = input("""Chose one of the following: \n
    N -> Make a new entry \n
    S -> Search for an entry \n
    Q -> Quit\n
    -> """).lower().strip()
    if choice == 's':
        search_for_entry()
    elif choice == 'q':
        sys.exit()
    else:
        new_entry()


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def new_entry():
    """Make a new entry in the CSV file. New entry must include
    [Name], [Minutes Spent], [Date], and [Notes]"""
    clear_screen()
    task = {}
    task['Name'] = input('What is the name of your task? ')
    task['Minutes Spent'] = input('How many minutes total did you spend on this task? ')
    if input('Would you like to add notes for this task? ').lower() == 'y':
        task['Notes'] = input('Please type your notes: ')
    Entry.create(title=task['Name'], time_spent=task['Minutes Spent'], notes=task['Notes'])
    clear_screen()
    input('Task saved! Please hit any key to return to the main menu')
    display_menu()


def search_for_entry():
    """Display menu with options for searching for an entry these
    options include searching by [Date], [Time Spent], [Exact Search]
    and [Regex Pattern]"""
    clear_screen()
    choice = input('''
    How would you like to search?
    D -> Search by date
    T -> Search by time spent
    N -> Search by task name
    P -> Search by Regex pattern

    M -> Return to main menu
    ''').lower().strip()

    if choice == "d":
        search_by_date()
    elif choice == "t":
        search_by_time_spent()
    elif choice == "n":
        search_exact()
    elif choice == "p":
        search_by_pattern()
    else:
        display_menu()


def search_by_date():
    """Allows user to search for tasks by a date
    NEED TO UPDATE TO WORK WITH DATABASE!"""
    clear_screen()
    results = []
    date_given= input("Please enter the date you want to search for tasks from. Please"
          "use the format MM-DD-YYYY ")
    if re.search(r'\d{2}-\d{2}-\d{4}', date_given):
        with open('entries.csv') as csvfile:
            csv_dict = csv.DictReader(csvfile)
            for entry in csv_dict:
                if date_given in entry['Date']:
                    results.append(entry)
    else:
        print("Sorry, that's not a date I recognize. Please try again.")
        search_by_date()
    if results:
        display_entries(results)
        input("That's all I could find. Press any key to return to the search menu")
        search_for_entry()
    else:
        clear_screen()
        input("No results were found for your search. Press any key to return to search menu.")
        search_for_entry()


def search_by_time_spent():
    """Allows user to search for tasks by number of minutes spent on
    task. NEED TO UPDATE TO WORK WITH DATABASE!"""
    clear_screen()
    results = []
    time_given = input("Search for tasks that took how many minutes? Please"
                       "convert all time to minutes > ")
    if re.search(r'\d+', time_given):
        with open('entries.csv') as csvfile:
            csv_dict = csv.DictReader(csvfile)
            for entry in csv_dict:
                if time_given in entry['Minutes Spent']:
                    results.append(entry)
    else:
        print("Sorry, that's not a valid entry. Please try again.")
        search_by_time_spent()
    if results:
        display_entries(results)
        input("That's all I could find. Press any key to return to the search menu")
        search_for_entry()
    else:
        clear_screen()
        input("Sorry, no results were found for your entry. Press any key to return to the search menu")
        search_for_entry()


def search_exact():
    """Allows user to search by the exact name of the task. NEED TO UPDATE TO WORK WITH DATABASE!"""
    clear_screen()
    results = []
    text = input("Please enter part or the full name of a task to search for > ")
    if text:
        with open('entries.csv') as csvfile:
            csv_dict = csv.DictReader(csvfile)
            for entry in csv_dict:
                if text in entry['Name']:
                    results.append(entry)
    else:
        print("Sorry, you didn't enter anything. Please try again.")
        search_exact()
    if results:
        display_entries(results)
        input("That's all I could find. Press any key to return to the search menu")
        search_for_entry()
    else:
        clear_screen()
        input("Sorry, no results were found for your entry. Press any key to return to the search menu.")
        search_for_entry()


def search_by_pattern():
    """Allows user to provide a RegEx pattern to search for tasks. NEED TO UPDATE TO WORK WITH DATABASE!"""
    clear_screen()
    results = []
    pattern = input("Please enter the regex pattern you wish to search with > ")
    compile_pattern = re.compile(r''+pattern)
    if pattern:
        with open('entries.csv') as csvfile:
            csv_dict = csv.DictReader(csvfile)
            for entry in csv_dict:
                if pattern.findall(entry):
                    results.append(entry)
    else:
        clear_screen()
        input("Sorry, that wasn't a valid entry. Press any key to try again")
        search_by_pattern()
    if results:
        display_entries(results)
        input("That's all I could find. Press any key to return to the search menu")
        search_for_entry()
    else:
        clear_screen()
        input("Sorry, no results were found for your entry. Press any key to return to the search menu.")
        search_for_entry()


def display_entry(entry):
    """Displays one entry"""
    print("*" * 50)
    print("Date and time: {}".format(entry['Date']))
    print("Task name: {}".format(entry['Name']))
    print("Minutes spent: {}".format(entry['Minutes Spent']))
    if entry['Notes']:
        print("Notes: {}".format(entry['Notes']))
    print("*" * 50)


def display_entries(entries):
    """Used for returning search results. Can be paged through. Also
    provides options to editing an entry, deleting an entry, and returning
    to the main menu"""
    print("Based on your search I found {} entries".format(len(entries)))
    count = 0
    while count < len(entries):
        display_entry(entries[count])
        entry = entries[count]
        print("\n")
        choice = input("""
        What would you like to do?
        E -> Edit this entry (feature coming in a later update)
        D -> Delete this entry (feature coming in a later update)
        P -> View previous entry
        N -> View next entry
        S -> Return to search menu
        """).strip().lower()
        if choice == "e":
            edit_entry(entry)
        elif choice == "d":
            delete_entry(entry)
        elif choice == "p":
            count -= 1
        elif choice == "s":
            search_for_entry()
        elif choice == "n":
            count += 1
        else:
            print("That's not a valid choice, start again")
            display_entries(entries)
    if count > len(entries):
        input("That's all the entries I could find. Press any key to return to the search menu")
        search_for_entry()


def delete_entry(entry):
    """Removes a specified entry from the CSV file"""
    print("You reached the delete entry section. This feature is under construction.")


def edit_entry(entry):
    """Allows user to change any field of a passed in entry"""
    print("You reached the edit entry section. This feature is under construction")



if __name__ == "__main__":
    run_program()
    display_menu()
