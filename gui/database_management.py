import logging as log
import sys

import psycopg2
from PyQt5.QtWidgets import QTableWidgetItem
import errors as ERRORS


class db_manager:

    def __init__(self, db_user, db_name):
        """
        Database initialization method

        :param db_user string: name of the user for the database
        :param db_name string: name of the database to connect to
        """
        # VITAL: The database has no password in its current implementation

        # Try to connect to database
        try:
            self.con = psycopg2.connect(user=db_user, dbname=db_name)

        except (Exception, psycopg2.OperationalError) as e:
            error = "DATABASE error: {}".format(e)
            log.error(error)  # Report connection error
            sys.exit()  # Exit program due to connectivity failure

        # Execute commands are automatically committed to the database
        self.con.autocommit = True
        self.cur = self.con.cursor()  # Create a cursor
        log.info("Connected to database : {}".format(db_name))

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

    def con_table(self, table_name, table_array=None, default_profile=None):
        """
        Method to connect to a table in database and crete table object

        :param table_name string: name of table to connect to
        :param table_array 2D_string_array: parameters list for desired table
        :param default_profile string_array: array containing parameters for default profile
        """
        try:
            # Try to create a new table object
            new_table = table(table_name, self.con, self.cur, default_profile)
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
                return table(table_name, self.con, self.cur, default_profile)

            else:
                log.error("Cannot generate table {0}.".format(table_name))
                sys.exit()


class table:

    def __init__(self, table_name, connection, cursor, default_profile):
        """
        Method to initialize a table object

        :param table_name string: name of current table
        :param connection psycopg2_connection_object: database connection
        :param cursor psyvcopg2_cursor_object: database cursor object
        :param default_profile string_array: array containing parameters for default profile
        """
        self.name = table_name
        self._connection = connection
        self._cursor = cursor
        self._default_profile = self._create_default_profile(default_profile)
        self._table_dict = self._get_table_dict()
        try:
            self._selected_row = self._table_dict[0]
        except KeyError:
            self._selected_row = None

        log.info("Connected to table : {}".format(table_name))

    def _create_default_profile(self, default_profile):
        """
        Hidden method to convert the default profile into a dctionary

        :param default_profile string_array: array containing parameters for default profile
        """
        columns = self._get_columns()
        dictionary = dict(zip(columns, default_profile))  # Create dictionary
        return dictionary

    def _get_columns(self):
        """
        Hidden method to get the columns from the table. Returns it as a 2d array

        """
        # Retrieve all data from the table
        self._cursor.execute("SELECT * FROM {0}".format(self.name))

        # Retrieve only the column titles
        columns = [cn[0] for cn in self._cursor.description]

        for i in range(len(columns)):  # Log the column names
            log.debug("Column {0} : {1}".format(i, columns[i]))

        return columns

    def _get_rows(self):
        """
        Hidden method to get the rows from the table

        """
        self._cursor.execute("SELECT * FROM {0}".format(self.name))
        rows = self._cursor.fetchall()

        # If we have no row and we are in the user_logins table
        if len(rows) == 0:
            log.warning("No row data found in {0}".format(self.name))
            log.info("Generating base admin user")
            self._selected_row = self._default_profile
            self.add_row()  # Add new row
            rows = self._cursor.fetchall()  # Refetch rows

        for i in range(len(rows)):  # Log rows
            log.debug("Rows {0} : {1}".format(i, rows[i]))

        # Sort the rows based on primary key
        rows = sorted(rows, key=lambda x: x[:][0])
        return rows

    def _get_table_dict(self):
        """
        Hidden method to generate a dict of rows which are dictionarys

        The calling method is a dict of rows enumarated at 0 for keys

        To call the relevant values to that row use the dict

        """
        temp_list = []  # Create a temporary empty list
        rows = self._get_rows()
        columns = self._get_columns()
        for row in rows:
            dictionary = dict(zip(columns, row))  # Create dictionary
            temp_list.append(dictionary)  # Append to the empty list

        dict_of_rows = {i: temp_list[i] for i in range(len(temp_list))}
        return dict_of_rows

    def add_row(self):
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

        columns = self._get_columns()

        if self._selected_row is None:  # If is no array of values
            log.error("No entries to add to rows")
            return False

        query = "INSERT INTO {0}(".format(self.name)

        for i in range(len(columns)):
            if i+1 != len(columns):
                query += columns[i] + ", "
            else:
                query += columns[i] + ") VALUES("

        for i, value in enumerate(self._selected_row.values()):
            if i+1 != len(columns):
                query += "{}, ".format(value)
            else:
                query += "{});".format(value)

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
                .format(self.name, self._get_columns()[0], primary_key)
        self.update_table(query)

    def edit_row(self, primary_key):
        """
        Method to edit a row in the table

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

        columns = self._get_columns()

        query = "UPDATE {0} SET".format(self.name)

        for i, value in enumerate(self._selected_row.values()):
            if i+1 == len(columns):
                query += " {0}={1} ".format(columns[i], value)
            else:
                query += " {0}={1},".format(columns[i], value)

        query += "WHERE {0}={1};".format(columns[0], primary_key)
        self.update_table(query)

    def update_table(self, query):
        """
        Method to execute a query and update the self.rows and self.columns

        :param query string: The SQL query which to perform
        """
        log.debug("Query : {}".format(query))
        self._cursor.execute(query)
        self._table_dict = self._get_table_dict()

    def check_unique(self, column_name, entry, entry_type):
        """
        Method to check if parameter is unique

        :param column_name string: column name to check for uniqueness
        :param entry various: value to check for uniqueness
        :param entry_type various: type of entry
        """
        # Check if column name is valid
        if not self._validate_column_name(column_name):
            raise AttributeError("{} is not a column name".format(column_name))
        try:
            if entry_type == int:
                entry = abs(int(entry))

            for row in self._table_dict.values():
                # If the value is not unique
                if entry == row[column_name]:
                    return False
            else:
                return True

        except ValueError:
            return None

    def change_data(self, column_name, entry, entry_type):
        """
        Method to change the data in the selected row

        :param column_name string: name of the column to edit
        :param entry various: value to insert into the column
        :param entry_type various: type of entry
        """
        # Validate the column name
        if not self._validate_column_name(column_name):
            raise AttributeError("{} is not a column name".format(column_name))

        elif entry_type == int:
            entry = str(abs(int(entry)))
        elif entry_type == str:
            entry = "'{}'".format(entry)
        elif entry_type == float:
            entry = str(abs(float(entry)))

        self._selected_row[column_name] = str(entry)

    def validate_entry(self, column_names, entries, entry_types):
        """
        Method to ensure that entered values are valid

        :param column_names list: list of the column names
        :param entries list: list of the entries to validate
        :param entry_types list: list of the types of entries
        """
        # Validate all column names
        if len(column_names) != len(entries) or len(entry_types) != len(column_names):
            raise IndexError("Arrays are not of same length")

        if not self._validate_column_name(column_names):
            raise AttributeError("{} contains an invalid column name".format(column_names))
        try:

            for i in range(len(entries)):
                if entry_types[i] == int:
                    entries[i] = str(abs(int(entries[i])))

            for row in self._table_dict.values():
                valid_values = []
                for i in range(len(column_names)):
                    if entries[i] == row[column_names[i]]:
                        valid_values.append(True)

                # If all desired values are valid for a user
                if len(valid_values) == len(entries):
                    return True

            else:
                return False

        except ValueError("Uniqueness: incorrect entry type"):
            return None

    def get_value(self, row, column=None):
        """
        Method to return values from the table

        :param row string: the row to retrieve from the table
        :param column string: optional variable to specify the column
        """

        if column is None:
            return self._table_dict[row]
        else:
            return self._table_dict[row][column]

    def populate(self, qt_table):
        """
        Method to populate a QTableWidget with all values for the table

        :param qt_table QTableWidet: table to populate
        """

        columns = self._get_columns()
        rows = self._get_rows()

        # Dynamically set the table information
        qt_table.setColumnCount(len(columns))
        qt_table.setHorizontalHeaderLabels(columns)
        qt_table.setRowCount(len(rows))

        for i in range(len(rows)):
            for j in range(len(columns)):
                qt_table.setItem(
                        i, j, QTableWidgetItem(str(rows[i][j])))

    def check_max_user(self, max_users):
        """
        Method to check if max users is exceeded

        :param max_users int: maximum number of users
        """
        if len(self._table_dict) >= max_users:
            return False
        else:
            return True

    def _validate_column_name(self, column_names):
        """
        Hidden method to validate column names

        :param column_names list or string: column name(s) to validate
        """
        if isinstance(column_names, list):
            return any(elem in self._get_columns() for elem in column_names)
        else:
            column_name = column_names
            for column in self._get_columns():
                if column_name == column:
                    return True
            else:
                return False

    def check_values(self, value, lower_lim, upper_lim):
        """
        Check to ensure values are within range

        :param value float: value to check
        :param lower_lim float: lower limit to check
        :param upper_lim float: upper limit to check
        """
        value = float(value)
        lower_lim = float(lower_lim)
        upper_lim = float(upper_lim)
        if lower_lim > upper_lim:
            log.error("Lower lim > upper lim")
            raise AttributeError
        elif value < lower_lim or value > upper_lim:
            raise ValueError

    def ensure_admin(self, row_number, column):
        print(row_number)
        for i in range(len(self._table_dict)):
            if i == row_number:
                continue
            elif self._table_dict[i][column] is True:
                return True

    def find_row_number(self, param, column):
        for i in range(len(self._table_dict)):
            if self._table_dict[i][column] == param:
                return i

