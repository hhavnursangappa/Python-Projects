import sqlite3
from sqlite3 import Error
import os


class Database:
    def __init__(self):
        """Constructor for the Database class.
        Check the existing path for a '.db' file and set the attribute self.filename."""

        self.filename = None
        for f_name in os.listdir('.'):
            if f_name.endswith('.db'):
                self.filename = f_name
                break

        if self.filename is None:
            with open("password.db", 'w') as db_file:
                self.filename = 'password.db'
                db_file.close()

    # MASTER PASSWORD METHODS
    def sql_create_master_password_table(self, pwd):
        """Function to create a table and store the master password."""
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        if not self.is_master_table():
            c.execute(""" CREATE TABLE master_pwd_table (master_password TEXT) """)
            conn.commit()
        self.sql_insert_master_password(pwd)
        conn.commit()
        conn.close()

    def sql_insert_master_password(self, pwd):
        """Function to insert and save the master password for the first time."""
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" INSERT INTO master_pwd_table VALUES (:password) """, {'password': pwd})
        conn.commit()
        conn.close()

    def sql_update_master_pwd(self, new_pwd):
        """Function to update the master password."""
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        try:
            c.execute(""" UPDATE master_pwd_table SET master_password = :new_val """, {'new_val': new_pwd})
            conn.commit()
            conn.close()
            return True
        except Error as e:
            print("ERROR: " + str(e))
            return False

    def sql_return_master_password(self):
        """Function to return the master password for login authentication."""
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" SELECT * FROM master_pwd_table """)
        result = c.fetchall()
        conn.commit()
        conn.close()
        return result[0][0]

    # PASSWORD MANAGER METHODS
    def sql_create_password_table(self, sl_no, website, username, password):
        """Function to create and store the credentials entered by the user."""
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        if self.is_password_table():
            self.sql_insert_values(sl_no, website, username, password)
        else:
            c.execute(""" CREATE TABLE password_manager (sl_no INTEGER PRIMARY KEY, website TEXT, username TEXT, password TEXT) """)
            self.sql_insert_values(sl_no, website, username, password)
        conn.commit()
        conn.close()

    def sql_insert_values(self, sl_no, website, username, password):
        """Function to insert the credentials entered by the user into the password manager table."""
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" INSERT INTO password_manager VALUES (:num, :web, :user, :pass) """,
                 {'num': sl_no, 'web': website, 'user': username, 'pass': password})  # SQL statement to insert entries into a table
        conn.commit()
        conn.close()

    def sql_return_serial_number(self):
        """Function to generate serial numbers for every entry in the password manager table."""
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" SELECT * FROM password_manager """)
        result = c.fetchall()
        num = len(result)
        conn.commit()
        conn.close()
        return num+1

    def sql_update_credentials(self, sl_num, new_website, new_username, new_password):
        """Function to update the user credentials using the functions defined above."""
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" UPDATE password_manager SET website = :val, username=:user, password=:pass  WHERE sl_no = :num """,
                  {'val': new_website, 'user': new_username, 'pass': new_password, 'num': sl_num})
        conn.commit()
        conn.close()
        return True

    def sql_print_value(self, inp_arg):
        """Function to print a particular user credential to the terminal."""
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        if inp_arg is None:
            raise TypeError("Please enter a sl. no. of the entry")
        else:
            c.execute(""" SELECT * FROM password_manager WHERE sl_no=:num """, {'num': inp_arg})
            values = c.fetchall()
            conn.commit()
            conn.close()

            return values

    def sql_return_all_values(self):
        """Function to print all user credentials to the terminal."""
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        if self.is_password_table():
            c.execute(""" SELECT * FROM password_manager """)  # SQL command to select all entries in a table
        else:
            c.execute(""" CREATE TABLE password_manager (sl_no INTEGER PRIMARY KEY, website TEXT, username TEXT, password TEXT) """)
            c.execute(""" SELECT * FROM password_manager """)
        values = c.fetchall()
        conn.commit()
        conn.close()
        return values

    def sql_remove_values(self, inp_arg):
        """Function to remove a particular user from the database."""
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        if inp_arg is None:
            raise TypeError(" Please provide a field to remove ")
        else:
            c.execute(""" SELECT * FROM password_manager """)
            len_table = len(c.fetchall())

            c.execute(""" SELECT * FROM password_manager WHERE sl_no BETWEEN :start AND :end """,
                      {'start': inp_arg + 1, 'end': len_table})
            conn.commit()
            next_entries = c.fetchall()
            c.execute(""" DELETE FROM password_manager WHERE sl_no=:num """, {'num': inp_arg})
            conn.commit()
            for entry in next_entries:
                c.execute(""" UPDATE password_manager SET sl_no = sl_no -1 WHERE sl_no = :num """, {'num': entry[0]})
            conn.commit()
            conn.close()
            return True

    def sql_remove_all_values(self):
        """Function to remove all user credentials from the database."""
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        if self.is_password_table():
            c.execute(""" DELETE FROM password_manager """)  # SQL command to delete all entries from a table
            conn.commit()
            conn.close()
        else:
            conn.close()

    # CHECK FUNCTIONS
    def is_password_table(self):
        """Function to check if the password manager table is present or not."""
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        try:
            c.execute(""" SELECT name FROM sqlite_master WHERE type='table' and name='password_manager' """)
            chk_res = c.fetchall()
            conn.commit()
            conn.close()
            if len(chk_res) != 0:
                return True
            else:
                return False
        except Error as e:
            print("ERROR: " + str(e))
            return False

    # def is_password_data(self):
    def is_password_table_empty(self):
        """Function to check if password data is in password manager table."""
        if self.is_password_table():
            conn = sqlite3.connect(self.filename)
            c = conn.cursor()
            c.execute(""" SELECT * FROM password_manager """)
            chk_res = c.fetchall()
            # print(table_data)
            conn.commit()
            conn.close()
            if len(chk_res) != 0:
                return True
            else:
                return False
        else:
            return False

    def is_master_table(self):
        """Function to check if the master password table is present or not."""
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        try:
            c.execute(""" SELECT name FROM sqlite_master WHERE type='table' and name='master_pwd_table' """)
            # c.execute(""" SELECT * FROM master_pwd_table """)
            chk_res = c.fetchall()
            # print(table_name)
            conn.commit()
            conn.close()
            if len(chk_res) != 0:
                return True
            else:
                return False
        except Error as e:
            print("ERROR: " + str(e))
            return False

    def is_master_table_empty(self):
        """Function to check if passwords are present in the master password table."""
        if self.is_master_table():
            conn = sqlite3.connect(self.filename)
            c = conn.cursor()
            c.execute(""" SELECT * FROM master_pwd_table """)
            chk_res = c.fetchall()
            conn.commit()
            conn.close()
            if len(chk_res) == 0:
                return True
            else:
                return False
        else:
            return False
