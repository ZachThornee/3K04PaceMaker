import psycopg2
import sys
import logging as log


class db_manager:

    def __init__(self, user, database_name):
        """
        Database initialization method

        :param user string: name of the user for the database
        :param database_name string: name of the database to connect to
        """
        # VITAL: The database has no password in its current implementation
        self.user = user
        self.db_name = database_name

        # Try to connect to database
        try:
            self.con = psycopg2.connect(user=self.user, database=self.db_name)
        except (Exception, psycopg2.OperationalError) as e:
            error = "DATABASE error: {}".format(e)
            log.error(error)  # Report connection error
            sys.exit()  # Exit program due to connectivity failure

        # Execute commands are automatically committed to the database
        self.con.autocommit = True
        self.cur = self.con.cursor()  # Create a cursor
        log.info("Connected to database : {}".format(database_name))

    def create_table(self, table_name, info_array):
        """
        Method to create a table in the database

        :param table_name string: name of the table to create
        :param info_array 2D_string_array: contains all parameters for table

        r = row     a = argument    N = an arbitrary number
        ---------------------------------------------------------------

        CURRENT_QUERY_STRUCTURE: Before first iteration

        CREATE TABLE table_name(

        ---------------------------------------------------------------

        CURRENT_QUERY_STRUCTURE: After first iteration

        CREATE TABLE table_name(r1_a1 r1_aN,

        ---------------------------------------------------------------

        CURRENT_QUERY_STRUCTURE: After 2nd iteration

        CREATE TABLE table_name(r1_a1 r1_aN, r2_a1 r2_aN,

        ---------------------------------------------------------------

        CURRENT_QUERY_STRUCTURE: Final structure after loop

        CREATE TABLE table_name(r1_a1 r1_aN, r2_a1 r2_aN, rN_a1 rN_aN);
        """

        try:
            query = "CREATE TABLE {0}(".format(table_name)

            for i in range(len(info_array)):
                for j in range(len(info_array[i])):
                    query += info_array[i][j] + " "
                query = query.strip()
                if i+1 == len(info_array):  # If we are on the last iteration
                    query += ");"  # Close the query
                else:
                    query += ", "  # Continue the query

            self.cur.execute(query)
            log.info("Created table {}".format(table_name))

        except (Exception, psycopg2.DatabaseError) as e:
            """
            CAUSES OF ERRORS:

            -> Improperly formatted query, check info_array for errors
            """
            log.error("Cannot create table: {0} -> {1}".format(table_name, e))

    def delete_table(self, table_name):
        """
        Method to delete a table in the database

        :param table_name string: table to delete in database

        FINAL QUERY STRUCTURE:

        DELETE TABLE IF EXISTS table_name
        """
        self.cur.execute("DROP TABLE IF EXISTS {0}".format(table_name))

    def close_connection(self):
        """
        Method to close the database connection

        """
        if (self.con):
            self.cur.close()
            self.con.close()
            log.info("Database connection closed")

    def con_table(self, table_name, table_array=None):
        """
        Method to connect to a table in database and crete table object

        :param table_name string: name of table to connect to
        :param table_array 2D_string_array: parameters list for desired table
        """
        try:
            # Try to create a new table object
            new_table = table(table_name, self.con, self.cur)
            return new_table

        except (Exception, psycopg2.errors.UndefinedTable) as e:
            """
            CAUSES OF ERRORS:

            -> Structure of table does not match database
            -> The table does not exist
            """
            error = "Cannot connect to table {0} -> {1}".format(table_name, e)
            log.error(error)

            # If local structure of table is different to database
            if table_array is not None:
                log.info("Creating table {0}".format(table_name))
                self.delete_table(table_name)  # Delete database table
                self.create_table(table_name, table_array)  # Gen new table
                return table(table_name, self.con, self.cur)

            else:
                log.error("Cannot generate table {0}.".format(table_name))
                sys.exit()


class table:

    # Parameters to create an initial user.
    # VITAL: Does create in patient table. Only the doctor (user) database.
    admin_creds = ["0", "'admin'", "'admin'", "'admin'", "'admin'", "'admin'", "TRUE"]

    def __init__(self, table_name, connection, cursor):
        """
        Method to initialize a table object

        :param table_name string: name of current table
        :param connection psycopg2_connection_object: database connection
        :param cursor psyvcopg2_cursor_object: database cursor object
        """
        self.name = table_name
        self.connection = connection
        self.cursor = cursor
        self.columns = self.get_columns()  # Get columns
        self.rows = self.get_rows()  # Get rows
        self.changed_data = None
        log.info("Connected to table : {}".format(table_name))

    def get_columns(self):
        """
        Method to get the columns from the table

        """
        # Retrieve all data from the table
        self.cursor.execute("SELECT * FROM {0}".format(self.name))

        # Retrieve only the column titles
        columns = [cn[0] for cn in self.cursor.description]

        for i in range(len(columns)):  # Log the column names
            log.debug("Column {0} : {1}".format(i, columns[i]))

        return columns

    def get_rows(self):
        """
        Method to get the rows from the table

        """
        self.cursor.execute("SELECT * FROM {0}".format(self.name))
        rows = self.cursor.fetchall()

        # If we have no row and we are in the user_logins table
        if len(rows) == 0 and self.name == 'user_logins':
            log.warning("No row data found in {0}".format(self.name))
            log.info("Generating base admin user")
            self.add_row(self.admin_creds)  # Add new row
            rows = self.cursor.fetchall()  # Refetch rows

        for i in range(len(rows)):  # Log rows
            log.debug("Rows {0} : {1}".format(i, rows[i]))

        # Sort the rows based on employee number
        rows = sorted(rows, key=lambda x: x[:][0])
        return rows

    def get_table_dict(self):
        """
        Generate a dict of users which are dictionarys

        The calling method is a dict of users enumarated at 0 for keys

        To call the relevant values to that user use the dict

        """
        temp_list = []  # Create a temporary empty list
        for user in self.rows:
            dictionary = dict(zip(self.columns, user))  # Create dictionary
            temp_list.append(dictionary)  # Append to the empty list

        dict_of_users = {i: temp_list[i] for i in range(len(temp_list))}
        return dict_of_users

    def add_row(self, responses):
        """
        Method to add a row to a database table

        :param responses array_diff_types: array containing values for the row

        v = value   c = column  N = an arbitrary number
        -------------------------------------------------------

        CURRENT_QUERY_STRUCTURE: Before first column iteration

        INSERT INTO table_name(

        -------------------------------------------------------

        CURRENT_QUERY_STRUCTURE: After all columns added

        INSERT INTO table_name(c1, c2, cN

        -------------------------------------------------------

        BCURRENT_QUERY_STRUCTURE: Before first value iteration

        INSERT INTO table_name(c1, c2, cN) VALUES(

        -------------------------------------------------------

        CURRENT_QUERY_STRUCTURE: After all values added

        INSERT INTO table_name(c1, c2, cN) VALUES(v1, v2, vN);
        """

        if responses is None:  # If is no array of values
            log.error("No entries to add to rows")
            return False

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
                query += responses[i] + ");"

        self.update_table(query)

    def delete_row(self, primary_key):
        """
        Method to delete a row from a table

        :param primary_key int: Key that identifies table row
        """
        if primary_key is None:
            log.error("No primary key for delete row")
            return False

        query = "DELETE FROM {0} WHERE {1} = {2} " \
                .format(self.name, self.columns[0], primary_key)
        self.update_table(query)

    def edit_row(self, data, primary_key):
        """
        Method to edit a row in the table

        :param data array_diff_types: Array containing new row data
        :param primary_key type_of_primary_key: A primary key which to look in the table to change the row

        v = value   c = column  N = an arbitrary number
        -------------------------------------------------------

        CURRENT_QUERY_STRUCTURE: Before first iteration

        UPDATE table_name SET

        -------------------------------------------------------

        CURRENT_QUERY_STRUCTURE: After first iteration

        UPDATE table_name SET c1=v1,

        -------------------------------------------------------

        BCURRENT_QUERY_STRUCTURE: After second iteration

        UPDATE table_name SET c1=v1, c2=v2,

        -------------------------------------------------------

        CURRENT_QUERY_STRUCTURE: After all iterations

        UPDATE table_name SET c1=v1, c2=v2, cN=vN

        -------------------------------------------------------

        CURRENT_QUERY_STRUCTURE: Finished query

        UPDATE table_name SET c1=v1, c2=v2, cN=vN WHERE c0=primary_key;
        """

        if data is None:
            log.error("No data to insert into table")
            return False

        if primary_key is None:
            log.error("No primary_key to delete row")
            return False

        query = "UPDATE {0} SET".format(self.name)

        for i in range(len(self.columns)):
            if i+1 == len(self.columns):
                query += " {0}={1} ".format(self.columns[i], data[i])
            else:
                query += " {0}={1},".format(self.columns[i], data[i])

        query += "WHERE {0}={1};".format(self.columns[0], primary_key)
        self.update_table(query)

    def update_table(self, query):
        """
        Method to execute a query and update the self.rows and self.columns

        :param query string: The SQL query which to perform
        """
        log.debug("Query : {}".format(query))
        self.cursor.execute(query)
        self.columns = self.get_columns()
        self.rows = self.get_rows()
