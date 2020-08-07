# fromJSONtoDB
Created by Jakub Zasada.

This program was created for the internship assignment at the Profil Software company.
The program retrieves data from the json file, analyzes it and saves it in the sqlite3 database. Made in Python 3.8.2.

The program also removes the 'picture' field from the json file, clears the phone number and adds a column with the number of days until the user's birthday.

How to start:

1. Install Python 3
2. In the terminal upgrade pip: python -m pip install --upgrade pip
3. Then install needed libraries:
   pip install click
   pip install peewee
4. Download this repository.
5. In script.py you can set name of database or json file.
6. Type python script.py load-json  to run the code.

Available commands (type in the terminal):
1.  python script.py --help                                    +That will show all available commands.
2.  python script.py command --help                            +That will show you options for the command.
  
3.  python script.py load-json                                 +This is start command. This will load data from json and create database with them.
  
4.  python script.py average-age                               +Shows average age of all users.
5.  python script.py average-age-female                        +Shows average age of all women.
6.  python script.py average-age-male                          +Shows average age of all men.
7.  python script.py genders                                   +Shows the percentage of all genders.
8.  python script.py most-popular-city option                  +Shows the most popular cities. Example: python script.py most-popular-city --number=5  
                                                              That shows the 5 most popular cities and number of appearances.
9.  python script.py most-popular-password option              +Shows the most popular passwords. Example: python script.py most-popular-password --number=5  
                                                              That shows the 5 most popular passwords and number of appearances.                                            
10.  python script.py most-safe-password option                 +Shows the most safe passwords. Example: python script.py most-safe-password --number=5  
                                                              That shows the 5 most safe passwords and number of points. 
11.  python script.py birth-betwen option option                +Shows users born between these dates. Example: python script.py birth-betwen --date-from='1950-06-26' --date-to='2000-05-25'
                                                              That shows all users born between 1950-06-26 and 2000-05-25.
