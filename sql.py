import sqlite3
import excel_header as excel

class my_db_class():
    def __init__(self, db_name):
        self.name_db = db_name
        self.connection = sqlite3.connect(self.name_db)
        self.cursor = self.connection.cursor()


    def set_tablename(self, table_name):
        self.table_name = table_name


    def create_table_name(self):
        if not self.table_name:
            print(f"No se ha introducido el nombre de la tabla\n Use: set_tablename()\n")
            return
        
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'"
        self.cursor.execute(query)
        table_exists = self.cursor.fetchone()
        
        if table_exists:
            print(f" ERROR : The table '{self.table_name}' already exists \n")
            return
        
        # Creamos la tabla deseada
        # Variables
        column_name     = list(excel.sql_columns.keys())
        column_variable = list(excel.sql_columns.values())
        _total = len(column_name)

        query = f"CREATE TABLE {self.table_name} (ID INTEGER PRIMARY KEY, "
        for i, name_temp in enumerate(column_name):
            query += f"{column_name[i]} {column_variable[i]}"
            if i < _total -1:
                query += ", "
        query += ")"
        #print(f"Mensaje a enviar:\n{query}")
        self.cursor.execute(query)
        self.connection.commit()
        print(f"Se creo la tabla '{self.table_name}'\n")


    def delete_table(self):
        try:
            self.cursor.execute(f"DROP TABLE {self.table_name}")
            print(f"Table '{self.table_name}' has been deleted successfully.")
        except sqlite3.OperationalError as e:
            print(f"Delete_table ERROR: {e}")

        self.connection.commit()


    def insert_data_in_table(self, my_key_array, array_new_values):
        if  not isinstance(array_new_values, list):
            print(f"Error, input_variable is not an list array")
            return
        list_column = ",".join(my_key_array)
        numbers_parameters = len(my_key_array)
        incognitos_array = ["?"]*numbers_parameters
        incog = ",".join(incognitos_array)
        query = f"INSERT INTO {self.table_name} ({list_column}) VALUES ({incog})"
        print(f"-- {my_key_array}")
        print(f"-- {array_new_values}")
        try:
            self.cursor.execute(query, array_new_values)
            print(f" - Data agregada a la tabla {self.table_name} ")
        except Exception as e:
            print(f"Error in inser_data_in_table = {e}")

        self.connection.commit()


    def close(self):
        self.connection.close()




