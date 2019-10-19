import psycopg2
import sys
import logging as log


class db_manager:

    def __init__(self, user, database_name):
        self.user = user
        self.db_name = database_name

        # Try to connect to database
        try:
            self.con = psycopg2.connect(user=self.user, database=self.db_name)
        except (Exception, psycopg2.OperationalError) as e:
            error = "DATABASE error: {}".format(e)
            log.error(error)
            sys.exit()

        self.con.autocommit = True
        self.cur = self.con.cursor()
        log.info("Connected to database : {}".format(database_name))

    def create_table(self, table_name, info_array):
        try:
            query = "CREATE TABLE {0}(".format(table_name)

            for i in range(len(info_array)):
                for j in range(len(info_array[i])):
                    query += info_array[i][j] + " "
                query = query.strip()
                query += ", "

            query = query[:-2] + ");"

            self.cur.execute(query)
            log.info("Created table {}".format(table_name))

        except (Exception, psycopg2.DatabaseError) as e:
            log.error("Cannot create table: {0} -> {1}".format(table_name, e))

    def delete_table(self, table_name):
        self.cur.execute("DROP TABLE IF EXISTS {0}".format(table_name))

    def close_connection(self):
        if (self.con):
            self.cur.close()
            self.con.close()
            log.info("Database connection closed")

    def con_table(self, table_name, table_array=None):
        try:
            new_table = table(table_name, self.con, self.cur)
            return new_table

        except (Exception, psycopg2.errors.UndefinedTable) as e:
            error = "Cannot connect to table {0} -> {1}".format(table_name, e)
            log.error(error)
            if table_array is not None:
                log.info("Creating table {0}".format(table_name))
                self.delete_table(table_name)
                self.create_table(table_name, table_array)
                return table(table_name, self.con, self.cur)
            else:
                log.error("Cannot generate table {0}.".format(table_name))
                sys.exit()


class table:

    def __init__(self, table_name, connection, cursor):
        self.name = table_name
        self.connection = connection
        self.cursor = cursor
        self.columns = self.get_columns()
        self.rows = self.get_rows()
        log.info("Connected to table : {}".format(table_name))

    def get_columns(self):
        self.cursor.execute("SELECT * FROM {0}".format(self.name))
        columns = [cn[0] for cn in self.cursor.description]
        for i in range(len(columns)):  # Display the column names
            log.debug("Column {0} : {1}".format(i, columns[i]))
        return columns

    def get_rows(self):
        command = "SELECT * FROM " + str(self.name)
        self.cursor.execute(command)
        rows = self.cursor.fetchall()
        for i in range(len(rows)):  # Display the column names
            log.debug("Rows {0} : {1}".format(i, rows[i]))
        return rows

    def get_table_dictionary(self):
        """
        Generate a dictionary of users which are dictionarys

        The calling method is a dictionary of users enumarated at 0 for keys

        To call the relevant values to that user use the dictionary

        """
        temp_list = []  # Create a temporary empty list
        for user in self.rows:
            dictionary = dict(zip(self.columns, user))  # Create dictionary
            temp_list.append(dictionary)  # Append to the empty list

        dict_of_users = {i: temp_list[i] for i in range(len(temp_list))}
        return dict_of_users

    def add_row(self, responses):

        query = "INSERT INTO {0}(".format(self.name)

        for i in range(len(self.columns)):
            if i+1 != len(self.columns):
                query += self.columns[i] + ", "
            else:
                query += self.columns[i] + ") VALUES("

        for i in range(len(responses)):
            if i+1 != len(responses):
                query += responses[i] + ", "
            else:
                query += responses[i] + ")"

        self.update_table(query)

    def delete_row(self, row_number=None):
        if row_number is None:
            row_number = input("What user would you like to delete? : ")

        query = "DELETE FROM {0} WHERE {1} = {2} " \
                .format(self.name, self.columns[0], row_number)
        self.update_table(query)

    def update_table(self, query, ):
        log.debug("Query : {}".format(query))
        self.cursor.execute(query)
        self.columns = self.get_columns()
        self.rows = self.get_rows()
        return self.get_table_dictionary()
