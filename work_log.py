import os
import sys
import datetime
import re

import peewee

#db = peewee.SqliteDatabase('entries.db')
db = None

FIELDNAMES = ['ID','Name', 'Minutes Spent', 'Date', 'Notes']
TIMESTAMP_FORMAT = "%m-%d-%Y"

class Entry(peewee.Model):
    #title
    title = peewee.CharField(max_length=255)
    #time spent (in minutes)
    time_spent = peewee.IntegerField(default=0)
    #date that is auto generated at creation
    date = peewee.DateTimeField()
    #optional notes
    notes = peewee.TextField(null=True)
    employee = peewee.CharField(max_length=255)

    class Meta:
        database = db


def run_program(db_name='entries.db'):
    """Create the database if it doesn't already exist"""
    db = peewee.SqliteDatabase(db_name)
    db.connect()
    db.create_tables([Entry], safe=True)

def display_menu():
    clear_screen()
    choice = None
    print("What would you like to do? ")
    print("""Chose one of the following: \n
    N -> Make a new entry \n
    S -> Search for an entry \n
    Q -> Quit\n
    """)
    while choice != 'q':
        choice = input("-> ").lower().strip()
        if choice == 's':
            search_for_entry()
        elif choice == 'q':
            break
        else:
            new_entry()


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def new_entry(task=None):
    """Make a new entry in the database. New entry must include
    [Name], [Minutes Spent], [Date], and [Notes]"""
    clear_screen()
    if task == None:
        task = {}
        task['Name'] = input('What is the name of your task? ')
        task['Employee'] = input("What is the employee's name that worked on this task? ")
        task['Minutes Spent'] = input('How many minutes total did you spend on this task? ')
        task['Notes'] = None
        if input('Would you like to add notes for this task? ').lower() == 'y':
            task['Notes'] = input('Please type your notes: ')
    task['Timestamp'] = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
    Entry.create(title=task['Name'], time_spent=task['Minutes Spent'], date=task['Timestamp'],
                 notes=task['Notes'], employee=task['Employee'])
    clear_screen()
    if task == None:
        input('Task saved! Please hit any key to return to the main menu')
        display_menu()


def search_for_entry():
    """Display menu with options for searching for an entry these
    options include searching by [Date], [Time Spent], [Exact Search]
    and [Regex Pattern]"""
    clear_screen()
    print('''
    How would you like to search?
    D -> Search by date
    T -> Search by time spent
    N -> Search by task name
    P -> Search by employee name

    M -> Return to main menu
    ''')
    choice = input("-> ").lower().strip()
    if choice == "d":
        search_by_date()
    elif choice == "t":
        search_by_time_spent()
    elif choice == "n":
        search_exact()
    elif choice == "p":
        search_by_employee()
    else:
        display_menu()


def search_by_date():
    """
    Allows user to search for tasks by a date
    """
    clear_screen()
    results = []
    date_given= input("Please enter the date you want to search for tasks from. Please"
          "use the format MM-DD-YYYY ")
    if re.search(r'\d{2}-\d{2}-\d{4}', date_given):
        entries = Entry.select().where(Entry.date == date_given)
        for entry in entries:
            results.append(entry)
        print("I found {} entries for that date".format(len(results)))
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
    """
    Allows user to search for tasks by number of minutes spent on task.
    """
    clear_screen()
    results = []
    time_given = input("Search for tasks that took how many minutes? Please"
                       " convert all time to minutes > ")
    if re.search(r'\d+', time_given):
        entries = Entry.select().where(Entry.time_spent == time_given)
        for entry in entries:
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
    """Allows user to search by the exact name of the task."""
    clear_screen()
    results = []
    text = input("Please enter part or the full name of a task to search for. Task notes will also be searched > ")
    if text:
        entries = Entry.select().where(Entry.title.contains(text))
        entries_notes = Entry.select().where(Entry.notes.contains(text))
        for entry in entries:
            results.append(entry)
        for entry in entries_notes:
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


def search_by_employee(search=None):
    """Allows user to provide a RegEx pattern to search for tasks."""
    clear_screen()
    results = []
    if search == None:
        name = input("Please enter the employee name you wish to search for > ")
    else:
        name = search
    if name:
        entries = Entry.select().where(Entry.employee.contains(name))
        for entry in entries:
            results.append(entry)
    else:
        clear_screen()
        input("Sorry, that wasn't a valid entry. Press any key to try again")
        search_by_employee()
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
    print("Date and time: {}".format(entry.date))
    print("Task name: {}".format(entry.title))
    print("Minutes spent: {}".format(entry.time_spent))
    if entry.notes:
        print("Notes: {}".format(entry.notes))
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
            count += 1
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
    """Removes a specified entry from the database"""
    Entry.delete_instance(entry)
    print("You sucessfully deleted the entry")


def edit_entry(entry):
    """Allows user to change any field of a passed in entry"""
    pass



if __name__ == "__main__":
    run_program()
    display_menu()
