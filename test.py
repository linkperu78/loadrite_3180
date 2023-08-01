import sql
import re
import time

database_name = "datos_serial.db"
_port='/dev/ttyUSB0'
_baud_rate = 9600
_timeout = 0.5

data = ['ID777', 'TM16:59:11', 'DT21 JUL 23', 'SP1 Mineral', 'U1 Limpieza', 'U2 Tajo1', 'U3 V3', 'AD4 8.02', 'E', '']
#data = ['ID777', 'SP2 Desmonte', 'E', 'ID777', 'TM18:40:51', 'DT21 JUL 23', 'SP2 Desmonte', 'U1 Acumulacion', 'U2 Tajo1', 'U3 V3', 'ST2 21.02', 'E', '']

if __name__ == "__main__":
    my_sql_db = sql.my_db_class(database_name)
    my_sql_db.set_tablename("datos")
    my_sql_db.create_table_name()
    dictionary_serial = sql.excel.excel_dictionary
    secuencia_number = sql.excel.funcion_
    try:
        while True:           
            mensaje = data
            if len(mensaje) < 8:
                continue

            final_dictionary = {"test" : "delete"}
            
            serial_id = dictionary_serial.keys()
            for msg in mensaje:
                for key in serial_id:
                    if not key in msg:
                        continue
                    new_value = msg.split(key)[1]
                    
                    if (key == "ID"):
                        new_value = int(new_value)

                    if (key == "SP"):
                        new_value=new_value.split(" ")[1]

                    if (key == "TM"):
                        pos_x = mensaje.index(msg)
                        time_ = mensaje[pos_x + 1]
                        date_ = time_.split("DT")[1]
                        new_value = date_ + " " + new_value
                    
                    if key in secuencia_number.keys():
                        data_ = new_value.split(" ")
                        my_number = int(data_[0])
                        peso = float(data_[1])
                        final_dictionary["Secuencia"] = my_number
                        final_dictionary["Peso"] = peso
                        new_value = secuencia_number[key]

                    new_key = dictionary_serial[key]
                    final_dictionary[new_key] = new_value
                    break

            final_dictionary.pop("test")    
            insert_array_columns   = []
            insert_array_values    = []

            for key in final_dictionary.keys():
                insert_array_columns.append(key)
                insert_array_values.append(final_dictionary[key])
            my_sql_db.insert_data_in_table(insert_array_columns,insert_array_values)
            
            time.sleep(3)

    except Exception as e:
        print(f"Error en main = {e}")

    except KeyboardInterrupt:
        print("Lectura de datos seriales detenida.")

    finally:
        # Cerrar la conexión a la base de datos
        my_sql_db.close()





