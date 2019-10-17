import psycopg2
import sys
import logging as log
log.basicConfig(format="Database - %(levelname)s: %(message)s", level=log.INFO)

MAX_LOGINS = 10

class db_manager:

    def __init__(self, user, database_name):
        self.user = user
        self.db_name = database_name

        # Try to connect to database
        try:
            self.con = psycopg2.connect(user = self.user, database = self.db_name)
        except (Exception, psycopg2.OperationalError) as e:
            error = "\n\nCannot connect to database {0} -> {1}\n".format(self.db_name, e)
            log.error(error)
            sys.exit()

        self.con.autocommit=True
        self.cur = self.con.cursor()
        log.info("Connected to database : {}".format(database_name))

    def create_table(self, table_name, info_array):
        try:
            create_table_query = "CREATE TABLE {0}(".format(table_name)

            for i in range(len(info_array)):
                for j in range(len(info_array[i])):
                    create_table_query += info_array[i][j] +" "
                create_table_query = create_table_query.strip()
                create_table_query += ", "

            create_table_query = create_table_query[:-2]
            create_table_query +=");"

            self.cur.execute(create_table_query)
            log.info("Created table {}".format(table_name))
        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while creating PostgreSQL table", error)

    def delete_table(self, table_name):
        self.cur.execute("DROP TABLE IF EXISTS {0}".format(table_name))

    def close_connection(self):
        if (self.con):
            self.cur.close()
            self.con.close()
            log.info("Database connection closed")

    def connect_to_table(self, table_name, table_array=None):
        try:
            new_table = table(table_name, self.con, self.cur)
            return new_table
        except (Exception, psycopg2.errors.UndefinedTable) as e:
            error = "\n\nCannot connect to table {0} -> {1}\n".format(table_name, e)
            log.error(error)
            if table_array is not None:
                log.info("Creating table {0}".format(table_name))
                self.delete_table(table_name)
                self.create_table(table_name, table_array)
                return table(table_name, self.con, self.cur)
            else:
                log.error("Cannot generate table {0}. Exiting".format(table_name))
                sys.exit()

class table:

    def __init__(self, table_name, connection, cursor):
        self.name=table_name
        self.connection = connection
        self.cursor = cursor
        self.columns = self.get_columns()
        self.rows = self.get_rows()
        log.info("Connected to table : {}".format(table_name))

    def get_columns(self):
        self.cursor.execute("SELECT * FROM {0}".format(self.name))
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

    def get_table_dictionary(self):
        """
        A function which calls the postgresql database to create a dictionary of users which are dictionarys

        The calling method is a list of users enumarated at 0 for keys

        To call the relevant values to that user use the dictionary

        """
        temp_list = [] # Create a temporary empty list
        for user in self.rows:
            dictionary = dict(zip(self.columns, user)) #Create a tuple and then conver to a dictionary
            temp_list.append(dictionary) # Append to the empty list

        dict_of_users = {i : temp_list[i] for i in range(len(temp_list))}
        return dict_of_users

    def add_row(self, responses):

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
                query += responses[i] + ")"

        self.update_table(query)

    def delete_row(self, row_number=None):
        if row_number is None:
            row_number = input("What user would you like to delete? : ")

        query = "DELETE FROM {0} WHERE {1} = {2} ".format(self.name, self.columns[0], row_number)
        self.update_table(query)

    def update_table(self, query, ):
        log.debug("Query : {}".format(query))
        self.cursor.execute(query)
        self.columns = self.get_columns()
        self.rows=self.get_rows()
        return self.get_table_dictionary()

if __name__ == "__main__":
    database = db_manager("jeff", "3K04_Database")
    LOGINS_TABLE_PARAMETERS = [
                    ["EMPLOYEE_NUMBER", "INT", "PRIMARY", "KEY", "NOT", "NULL"],
                    ["USER_LOGIN", "TEXT", "NOT", "NULL"],
                    ["PASSWORD", "TEXT",  "NOT", "NULL"],
                    ["EMAIL", "TEXT", "NOT", "NULL"],
                    ["FIRST_NAME", "TEXT", "NOT", "NULL"],
                    ["LAST_NAME", "TEXT", "NOT", "NULL"],
                    ["ADMIN_PRIVELEGES", "BOOLEAN", "NOT", "NULL"],
                ]
    #database.delete_table("user_logins")
    table_name = database.connect_to_table("user_logins", LOGINS_TABLE_PARAMETERS)
    print(table_name.get_columns())
    print(table_name.get_rows())
    #table_name.add_row(["0", "'jeff'", "'jeff'", "'jeff@email.com'", "'jeff'", "'jeff'", "TRUE"])

    # database = db_manager("jeff", "3K04_Database")
    # table_name = database.connect_to_table("patient_info", PATIENT_LOOKUP_PARAMETERS)
    # table_name.add_row(["0", "'jeff'", "'jeff'", "'N123N'", "'M'", "20", "123456789" ])
    # print(table_name.get_columns())
    # print(table_name.get_rows())
