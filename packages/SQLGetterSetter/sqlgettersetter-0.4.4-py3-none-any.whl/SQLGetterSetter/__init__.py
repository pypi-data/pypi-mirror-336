from mysql.connector import connect, Error

class MainClass:
    def __init__(self, connection=None, connection_params=None):
        """Initialize the object with Connection and new empty Query."""
        self.connection = connection
        self.connection_params = connection_params  # Store connection params for reconnection
        self.query = ""
        self.sub_query_count = 0

    def connect(self):
        """Establize New Connection and Reconnects if the connection is unavailable."""
        if not self.connection or not self.connection.is_connected():
            try:
                self.connection = connect(**self.connection_params)
                print("Reconnected to the database.")
            except Error as err:
                print(f"Error reconnecting: {err}")
                self.connection = None
                
    def create_db(self, dbname):
        """Creating an Database"""
        self.query += f"CREATE DATABASE {dbname}"
        return self
    
    def drop_db(self, dbname):
        """Dropping an Database"""
        self.query += f"DROP DATABASE {dbname}"
        return self
    
    def backup_db(self, dbname, path):
        """Backup the Database into the specified path"""
        self.query += f"BACKUP DATABASE {dbname} TO DISK = {path}"  
        return self
    
    def create_table(self, table, *columns):
        """Creates a table with the specified columns."""
        self.query = f"CREATE TABLE {table} ({', '.join(columns)})"
        return self

    def add_column(self, table, *columns):
        """Adds one or more columns to the specified table."""
        self.query = f"ALTER TABLE {table} ADD ({', '.join(columns)})"
        return self

    def drop_column(self, table, *columns):
        """Drops one or more columns from the specified table."""
        self.query = f"ALTER TABLE {table} " + ", ".join(f"DROP COLUMN {col}" for col in columns)
        return self

    def drop_table(self, table):
        """Drops the specified table."""
        self.query = f"DROP TABLE {table}"
        return self

    def drop_view(self, view):
        """Drops the specified view."""
        self.query = f"DROP VIEW {view}"
        return self
    
    def truncate_table(self, table):
        """Truncates the specified table."""
        self.query = f"TRUNCATE TABLE {table}"
        return self 
    
    def create_index(self, table_name, *columns):
        """Creates an index on the specified columns of the table."""
        index_name = "idx_" + "_".join(col.lower() for col in columns)
        self.query = f"CREATE INDEX {index_name} ON {table_name} ({', '.join(columns)})"
        return self

    def create_view(self, view_name):
        """Creates a view with the specified SELECT query."""
        self.query = f"CREATE VIEW {view_name} AS "
        return self
    
    def show(self, key):
        """SHOW is used to retrive the information of the database."""
        self.query += f"SHOW {key}"
        return self
    
    def select(self, *columns):
        """SELECT the coloumns and Default to '*' ."""
        if columns == (' ',):
            self.query += "SELECT"
        else:
            self.query += "SELECT " + ", ".join(columns) if columns else "SELECT *"
        return self 
    
    def sub_select(self, *columns):
        """SELECT the coloumns and Default to '*' ."""
        self.sub_query_count += 1
        if columns == (' ',):
            self.query += "(SELECT"
        else:
            self.query += " (SELECT " + ", ".join(columns) if columns else " (SELECT *"
        return self
    
    def distinct(self, *columns):
        """DISTINCT is used to retrive the unique data , 
        Parameters are single and multiple column_names."""
        self.query += " DISTINCT " + ", ".join(columns)
        return self

    def where(self, *condition, operator=None):
        """WHERE is used to retrive the data with certain conditions, 
        Parameters are normal condition as string or multiple condition with logical operation."""
        if operator is None:
            self.query += " WHERE " + " ".join(condition)
        elif condition == (' ',):
            self.query += " WHERE "
        else:
            self.query += " WHERE " + f" {operator} ".join(condition)
        return self
    
    def orderby(self, *columns_with_order):
        """ORDERBY is used to arrange the result orderly, P
        arameters are passed as an tuples containing of (column_name, order). 
        default is column name which assigned as ASC."""
        order_str = ", ".join(
            f"{col} {ord}" if isinstance(col, tuple) else f"{col} ASC"
            for col, ord in columns_with_order
        )
        self.query += f" ORDER BY {order_str}"
        return self

    def like(self, pattern):
        """LIKE is used to filter the data that are matches the pattern, 
        Parameter is passed as string pattern."""        
        self.query += f" LIKE {pattern}"
        return self

    def isnull(self,key = None):
        """ISNULL is used to check the data's of the column is Null or not, 
        No Parameters are passed."""
        if key != None:
            self.query += f" ISNULL({key})"
        else:
            self.query += f" IS NULL"
        return self
    
    def isnotnull(self):
        """ISNOTNULL is used to check the data's of the column is not Null,"""
        self.query += " IS NOT NULL"
        return self
    
    def ifnull(self, key, value):
        """IFNULL is used to replace the Null values with the specified value,"""
        self.query += f" IFNULL({key}, {value})"
        return self

    def nullif(self, key, value):
        """NULLIF is used to replace the specified value with the Null values,"""
        self.query += f" NULLIF({key}, {value})"
        return self
    
    def coalesce(self, *values):
        """COALESCE is used to retrive the first non-null value from the list of values,"""
        self.query += " COALESCE(" + ', '.join(map(str, values)) + ')'
        return self
    
    def AS(self, name):
        """AS is used to assign the alias name to the column,"""
        self.query += f" AS {name}"
        return self
    
    def between(self, start, end):
        """BETWEEN is used to retrive the data from certain range, 
        Parameters are starting value and ending."""
        self.query += f" BETWEEN {str(start)} AND {str(end)}"
        return self

    def IN(self, *values):
        """IN is used to check the multiple columns, 
        Parameter are column_names passed as tuple."""
        value_list = ', '.join(f"'{value}'" for value in values)
        self.query += f" IN ({value_list})"
        return self

    def and_operator(self):
        """It is an AND operator the added between the query is user's wish to."""
        self.query += " AND"
        return self

    def or_operator(self):
        """It is an OR operator the added between the query is user's wish to."""
        self.query += " OR"
        return self

    def add_operator(self):
        """It is an + operator the added between the query is user's wish to."""
        self.query += " +"
        return self
    
    def comma(self):
        """It is an , operator the added between the query is user's wish to."""
        self.query += ","
        return self
    
    def avg(self, value):
        """AVG is used to retrive the average of the data,"""
        self.query += f" AVG({value})"
        return self

    def count(self, value):
        """COUNT is used to retrive the count of the data,"""
        self.query += f" COUNT({value})"
        return self
    
    def max(self, value):
        """MAX is used to retrive the maximum value from the data,"""
        self.query += f" MAX({value})"
        return self
    
    def min(self, value):
        """MIN is used to retrive the minimum value from the data,"""
        self.query += f" MIN({value})"
        return self
    
    def sum(self, value):
        """SUM is used to retrive the sum of the data,"""
        self.query += f" SUM({value})"
        return self

    def year(self, value):
        """YEAR is used to retrive the year from the date,"""
        self.query += f" YEAR({value})"
        return self

    def groupby(self, *columns):
        """GROUPBY is used to group the data based on the column_names,"""
        self.query += f" GROUP BY {', '.join(columns)}"
        return self
    
    def table(self, table_name):
        """Assign the table name to the query."""
        self.query += f" FROM {table_name}"
        return self
    
    def limit(self, n, offset=None):
        """LIMIT is used to retrive the certain number of data from table, 
        Parameters are no.of.rows and OFFSET to skip the no.of.begging_rows -> default to None."""
        self.query += f" LIMIT {n}" if offset is None else f" LIMIT {n} OFFSET {offset}"
        return self

    def fetch(self, n, offset=None):
        """FETCH is used in sql_server to fetch certain amount of data, 
        Parameters are no.of.rows and OFFSET to skip the no.of.begging_rows -> default to None."""
        if offset is not None:
            self.query += f" OFFSET {offset} ROWS"
        self.query += f" FETCH NEXT {n} ROWS ONLY"
        return self
    
    def top(self, n, percent=False):
        """TOP is used in sql_server to retrive the begging data at certain percentage or number, 
        Parameters are no.of.rows and percentage default -> None."""
        replacement = f"SELECT TOP {n}{' PERCENT' if percent else ''}"
        self.query = self.query.replace("SELECT", replacement, 1)  
        return self
        
    def insert(self, table_name, values, columns=None):
        """
        Constructs an INSERT INTO SQL query for single or multiple rows.
        :param table_name: Name of the table to insert data into.
        :param values: List of values (single row as a tuple or multiple rows as a list of tuples).
        :param columns: List of column names (optional).
        """
        columns_part = f" ({', '.join(columns)})" if columns else ""        
        if isinstance(values, list):
            values_part = ", ".join(
                f"({', '.join(repr(value) if isinstance(value, str) else str(value) for value in row)})"
                for row in values
            )
        else:
            values_part = f"({', '.join(repr(value) if isinstance(value, str) else str(value) for value in values)})"
        
        self.query = f"INSERT INTO {table_name}{columns_part} VALUES {values_part}"
        return self

    def insert_into_select(self, source, destination, source_columns=None, destination_columns=None):
        """
        Constructs an INSERT INTO SELECT SQL query.

        :param source: Source table to select data from.
        :param destination: Destination table to insert data into.
        :param source_columns: List of source column names (optional).
        :param destination_columns: List of destination column names (optional).
        """
        source_columns_part = f" {', '.join(source_columns)}" if source_columns else "*"
        destination_columns_part = f" ({', '.join(destination_columns)})" if destination_columns else ""
        self.query = f"INSERT INTO {destination}{destination_columns_part} SELECT {source_columns_part} FROM {source}"
        return self
            
    def update(self, table_name, changes):
        """
        Constructs an UPDATE SQL query.
        :param table_name: Name of the table to update.
        :param changes: List of tuples containing column name and new value (e.g., [('column1', 'value1'), ('column2', 'value2')]).
        """
        if changes[0][1] == '':
            self.query += f"UPDATE {table_name} SET {changes[0][0]} ="
            return self
        else:
            if not isinstance(changes, list):
                raise ValueError("Changes must be a list of tuples: [('column1', 'value1'), ...]")
    
            def format_value(value):
                if isinstance(value, str):
                    return f"'{value.replace('\'', '\\\'')}'"
                return str(value)
            changes_part = ", ".join(f"{col} = {format_value(val)}" for col, val in changes)
            self.query = f"UPDATE {table_name} SET {changes_part}"
            return self

    def delete(self, table_name):
        """
        Constructs a DELETE SQL query.
        :param table_name: Name of the table to delete records from.
        :param condition: Optional condition for the WHERE clause (e.g., "id = 1").
        """
        self.query = f"DELETE FROM {table_name}"
        return self

    def select_into(self, source, destination, source_columns=None):
        """
        Constructs a SELECT INTO SQL query.
        :param source: Source table to select data from.
        :param destination: Destination table to insert data into.
        :param source_columns: List of column names to select (optional).
        """
        columns_part = ", ".join(source_columns) if source_columns else "*"
        self.query = f"SELECT {columns_part} INTO {destination} FROM {source}"
        return self
    
    def create_procedure(self, proc_name, queries, params=None):
        """
        Creates a stored procedure with the given name, queries, and optional parameters.
        
        :param proc_name: Name of the stored procedure.
        :param queries: List of SQL queries to include in the procedure.
        :param params: Optional parameters for the procedure (default is None).
                       Should be a list of strings, e.g., ["IN param1 INT", "OUT param2 VARCHAR(50)"].
        :param symbol: Delimiter symbol (default is '//').
        :return: Instance of the class (self).
        """
        param_string = ", ".join(params) if params else ""    
        query_body = "\n    ".join(queries)    
        self.query = f"""
CREATE PROCEDURE {proc_name}({param_string})
BEGIN
    {query_body}
END
"""
        return self
    
    def call_procedure(self, procedure_name, params=()):
        """Calls a stored procedure with the given name and parameters.
        Pass parameters as a tuple, e.g., ("param1", "param2")."""
        self.connect()
        if not self.connection:
            print("Connection is unavailable. Query cannot be executed.")
            return None
# 
        cursor = self.connection.cursor()
        try:
            cursor.callproc(procedure_name, params)
            results = []
            for result in cursor.stored_results():
                results.append(result.fetchall())
            cursor.close()
            self.query = ""
            return results
        except Error as err:
            print(f"Error: {err}")
            self.query = ""
            return None
    
    
    
    def exe(self):
        """Executes the constructed query."""
        self.connect()  # Ensure connection is available
        if not self.connection:
            print("Connection is unavailable. Query cannot be executed.")
            return None
# 
        cursor = self.connection.cursor()
        try:
            if self.sub_query_count > 0:
                cursor.execute(self.query + ');')
                self.sub_query_count = 0
            elif self.query.lower().startswith("create procedure"):
                cursor.execute(self.query)
                self.connection.commit()
            else:
                cursor.execute(self.query + ';')
            if self.query.lower().startswith("select"): #Need to return the Resulted data
                results = cursor.fetchall() 
            else:
                self.connection.commit()
                results = f"Query executed successfully, affected rows: {cursor.rowcount}"
            cursor.close()
            self.query = ""
            return results #Return as List or String
        except Error as err:
            print(f"Error: {err}")
            self.query = ""
            return None
            
            
            
            
