import logging as log
import random
import sys

import psycopg2
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

# Global configuration
DATABASE_NAME = "3K04_Database"
USER = "jeff"
LOGINS_TABLE = "user_logins"
INFO_ARRAY = [["name", "id", "login"]]
log.basicConfig(format='%(levelname)s: %(message)s', level=log.INFO)

class db_manager:

    def __init__(self, user, database_name):
        self.user = user
        self.db_name = database_name
        self.con = psycopg2.connect(user = self.user,
                                            database = self.db_name)
        self.con.autocommit=True
        self.cur = self.jon.cursor()
        log.info("Connected to database : {}".format(database_name))

    def create_table(self, table_name, info_array):
        try:
            create_table_query = "CREATE TABLE {0}(".format(table_name)

            for column in INFO_ARRAY:
                for i in range(len(column)):
                    if i+1 == len(column):
                        create_table_query += column[i] +", "
                    else:
                        create_table_query += column[i] +" "

            create_table_query +=");"

            desired_query = '''CREATE TABLE {0}(
                ID INT PRIMARY  KEY     NOT NULL,
                MODEL           TEXT    NOT NULL,
                PRICE           REAL);'''.format(table_name)

            print(create_table_query)
            print(desired_query)

            #self.cur.execute(create_table_query)
            self.cur.execute(desired_query)
            log.info("Created table {}".format(table_name))
        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while creating PostgreSQL table", error)

    def delete_table(self, table_name):
        command = "DROP TABLE IF EXISTS " + str(table_name)
        self.cur.execute(command)

    def close_connection(self):
        if (self.con):
            self.cur.close()
            self.con.close()
            log.info("Database connection closed")

    def connect_to_table(self, table_name):
        new_table = table(table_name, self.con, self.cur)
        return new_table


class table:

    def __init__(self, table_name, connection, cursor):
        self.name=table_name
        self.connection = connection
        self.cursor = cursor
        self.columns = self.get_columns()
        self.rows = self.get_rows()
        log.info("Connected to table : {}".format(table_name))

    def get_columns(self):
        self.cursor.execute('SELECT * FROM {0}'.format(self.name))
        columns= [cn[0] for cn in self.cursor.description]
        for i in range(len(columns)): # Display the column names
            log.debug("Column {0} : {1}".format(i, columns[i]))
        return columns

    def get_rows(self):
        command = "SELECT * FROM " + str(self.name)
        self.cursor.execute(command)
        rows = self.cursor.fetchall()
        for i in range(len(rows)): # Display the column names
            log.debug("Rows {0} : {1}".format(i, rows[i]))
        return rows

    def display_table(self):
        print("{:30}".format(self.name))

        string = ""
        for column in self.columns:
            string += "{:<20}".format(column)
        print(string)

        for row in self.rows:
            string = ""
            for element in row:
                string += "{:<20}".format(element)
            print(string)

    def add_row(self, responses=None):
        if responses is None:
            responses = []
            responses.append(str(len(self.rows)+1))
            for i in range(1,len(self.columns)):
                responses.append(input("{0} : ".format(self.columns[i])))

        if len(responses) != len(self.columns):
            log.warning("Incorrect response array. Please try again.")
            return None

        query = "INSERT INTO {0}(".format(self.name)

        for i in range(len(self.columns)):
            if i+1 != len(self.columns):
                query += self.columns[i] + ", "
            else:
                query +=self.columns[i] + ") VALUES("

        for i in range(len(responses)):
            if i+1 != len(responses):
                query += responses[i] + ", "
            else:
                query +=responses[i] + ")"

        self.update_table(query)

    def delete_row(self, row_number=None):
        if row_number is None:
            row_number = input('What user would you like to delete?')

        query = "DELETE FROM {0} WHERE {1} = {2} ".format(self.name, self.columns[0], row_number)
        self.update_table(query)

    def update_table(self, query, show_table=False):
        DIFFERENTIATOR = 10000
        log.debug("Query : {}".format(query))
        self.cursor.execute(query)

        # Increase all values
        self.columns = self.get_columns()
        self.rows=self.get_rows()
        for i in range(len(self.rows)):
            if self.rows[i][0] != i:
                query = "UPDATE {0} SET {1} = {2} WHERE {1} = {3}".format(self.name, self.columns[0], i+DIFFERENTIATOR, self.rows[i][0])
                log.debug("Query : {}".format(query))
                self.cursor.execute(query)

        # Reset all values
        self.columns = self.get_columns()
        self.rows=self.get_rows()
        for i in range(len(self.rows)):
            if self.rows[i][0] != i:
                query = "UPDATE {0} SET {1} = {2} WHERE {1} = {3}".format(self.name, self.columns[0], i, self.rows[i][0])
                log.debug("Query : {}".format(query))
                self.cursor.execute(query)

        self.columns = self.get_columns()
        self.rows=self.get_rows()
        if show_table:
            self.display_table()

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Protect your heart'
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 140

        # Connect to database manager
        try:
            self.db_man = db_manager(USER, DATABASE_NAME)
        except (Exception, psycopg2.OperationalError) as ERROR:
            error = "\n\nCannot connect to database {0} -> {1}\n".format(DATABASE_NAME, ERROR)
            log.error(error)
            sys.exit()

        # Connect to user logins table
        try:
            self.logins_table = self.db_man.connect_to_table(LOGINS_TABLE)
        except (Exception, psycopg2.errors.UndefinedTable) as ERROR:
            error = "\n\nCannot connect to table {0} -> {1}\n".format(LOGINS_TABLE, ERROR)
            log.error(error)
            sys.exit()

        # Connect to login window
        self.login_window()

    def login_window(self):
        # Title label
        self.title_label = QLabel("Login", self)
        self.title_label.move(20, 20,)
        self.title_label.resize(280, 40)

        # Username textbox
        self.username_textbox = QLineEdit(self)
        self.username_textbox.move(160, 80)
        self.username_textbox.resize(280, 40)

        # Username label
        self.username_label = QLabel("Username", self)
        self.username_label.move(20, 80)
        self.username_label.resize(280, 40)

        # Password Textbox
        self.password_textbox = QLineEdit(self)
        self.password_textbox.move(160, 140)
        self.password_textbox.resize(280, 40)

        # Password label
        self.password_label = QLabel("Password", self)
        self.password_label.move(20, 140)
        self.password_label.resize(280, 40)

        # Confirm login button
        self.confirm_button = QPushButton("Confirm", self)
        self.confirm_button.move(20, 200)
        self.confirm_button.resize(280, 40)
        self.confirm_button.clicked.connect(self.validate_user)

        # Manage users button
        self.add_users_button = QPushButton("Manage Users", self)
        self.add_users_button.move(20, 260)
        self.add_users_button.resize(280, 40)
        self.add_users_button.clicked.connect(self.manage_users_window)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def validate_user(self):
        username = self.username_textbox.text()
        password = self.password_textbox.text()

    def manage_users_window(self):
        print("connected to window")

if __name__ == "__main__":
    database_manager = db_manager(USER, DATABASE_NAME)
    database_manager.create_table(LOGINS_TABLE, INFO_ARRAY)
    #database_manager.delete_table(LOGINS_TABLE)
    #database_manager.create_table(LOGINS_TABLE, INFO_ARRAY)
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    #db = db_manager(USER, DATABASE_NAME)
    #table = db.connect_to_table(TABLE_NAME)
