from PyQt5.QtWidgets import QApplication, QLabel
import psycopg2
import logging as log

DATABASE_NAME = "3K04_Database"
USER = "jeff"
TABLE_NAME = "user_logins"
INFO_ARRAY = [[]]

class database_manager:

    def __init__(self, user, database_name):
        self.user = user
        self.db_name = database_name
        self.connection = psycopg2.connect(user = self.user,
                                            database = self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self, name, info_array):
        try:
            create_table_query = '''CREATE TABLE user_logins(
                ID INT PRIMARY  KEY     NOT NULL,
                MODEL           TEXT    NOT NULL,
                PRICE           REAL); '''
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("Created table")
        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while creating PostgreSQL table", error)

    def delete_table(self, table_name):
        command = "DROP TABLE IF EXISTS " + str(table_name)
        self.cursor.execute(command)
        self.cursor.commit()

    def fetch_all_info(self, table_name):
        command = "SELECT * FROM " + str(table_name)
        self.cursor.execute(command)
        self.cursor.fetchall()
        self.cursor.commit()

    def close_connection(self):
        if (self.connection):
            self.cursor.close()
            self.connection.close()
            log.info("Database connection closed")

class main_window(object):
    def __init__(self):
        self.label = QLabel('Hello World!')
        self.label.show()

if __name__ == "__main__":
    program = QApplication([])
    window = main_window()
    db = database_manager(USER, DATABASE_NAME)
    db.create_table(TABLE_NAME, INFO_ARRAY)
    db.close_connection()
