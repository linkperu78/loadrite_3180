import json
import time

def leer_json(direction_json):
    with open(direction_json, 'r') as json_file:
        data = json.load(json_file)
    return data

def byte_to_decimal_invert(byte):
    hex_base = ''.join(byte[::-1])
    return int( hex_base, 16 )

def print_dictionary(dictionary):
    print(f"\n------------\n Dictionary \n------------\n{{")
    for key in dictionary.keys():
        print(f"  {key} : {dictionary[key]}")
    print(f"\t}}\n")

# Esta clase nos permitira un mejor manejo de los eventos 
# obtenidos mediante la lectura del CANBUS
class loadrite_class():
    def __init__(self):
        self.peso_total     = 0
        self.peso_bucket    = 0
        self.iteration      = 0
        self.iteration_truck    = 0

    def upload_self_data(self, json_file):
        init_values = leer_json(json_file)
        keys = list(init_values.keys())
        self.material   = init_values[keys[0]]
        self.operation  = init_values[keys[1]]
        self.loading    = init_values[keys[2]]
        self.headers    = init_values[keys[3]]
        self.dictionary = init_values[keys[4]]

        
    # byte_loadrite = 3 - 6 bytes inverted of the array of CANBUS
    def actualizar_value_offset(self, byte_loadrite):
        offset = 2_147_483_648
        delta = byte_to_decimal_invert(byte_loadrite) - offset
        return delta

    # byte_loadrite = 2 -  bytes inverted of the array of CANBUS
    def actualizar_value(self, byte_loadrite):
        delta = byte_to_decimal_invert(byte_loadrite)
        return delta

    # Añadimos, restamos o deshacemos cambio en la cantidad
    # en el actual balde
    def bucket_event(self, pos_operation, byte_data):
        self.iteration += 1
        _pos = int(pos_operation, 16) -1  
        funcion         = self.operation[_pos]    # Add, rest or undo
        change_value    = self.actualizar_value_offset(byte_data)  # i.e: + 2350 kg, -650 kg
        self.peso_bucket    += change_value
        self.peso_total     += change_value
        self.dictionary["Funcion"]      = funcion 
        self.dictionary['Secuencia']    = self.iteration
        self.dictionary["Peso"]         = change_value


    # Actualizamos el material que se va a utilizar
    def product_event(self, byte_data):
        pos_item = int(byte_data,16) 
        if pos_item == 0:
            change_value = "Invalid product"
        else:
            change_value = self.material[pos_item - 1]
        self.dictionary["Producto"] = change_value

    # Se envia el total almacenado en el vessel
    def vessel_completed(self, data_byte):
        self.iteration += 1
        total_vessel = self.actualizar_value(data_byte)
        self.dictionary["Funcion"]      = "Vessel Completed"
        self.dictionary["Secuencia"]    = self.iteration
        self.dictionary["Peso"]         = total_vessel
        self.iteration = 0

    # Se envia el total almacenado en el truck
    def truck_completed(self, data_byte):
        self.iteration_truck += 1
        total_truck = self.actualizar_value(data_byte)
        self.dictionary["Funcion"]      = "Truck Completed"
        self.dictionary["Secuencia"]    = self.iteration_truck
        self.dictionary["Peso"]         = total_truck

    def hardreset(self):
        self.dictionary["Funcion"] = ""
        self.dictionary["Secuencia"] = 0
        self.dictionary["Peso"] = 0
        self.peso_total = 0
        self.iteration = 0
        self.peso_bucket = 0


    # Analizamos el byte del LoadRite3180 y realizamos una accion
    def get_action(self, canbus_byte):
        main_byte = int(canbus_byte[0] , 16)
        if not main_byte in self.headers:
            return 0

        if ( main_byte == int('0x00',16) ):     # Loading Cycle: 
            #print("Loading Cycle")
            self.hardreset()
            return 0
                    
        elif ( main_byte == int('0x01',16) ):
            #print("Bucket Event")
            status      = canbus_byte[1]
            data_byte   = canbus_byte[2:6]
            self.bucket_event(status, data_byte)
            return 1

        elif ( main_byte == int('0x02',16) ):
            #print("Vessel Completed")
            data_byte = canbus_byte[1:5]
            self.vessel_completed(data_byte)
            return 1

        elif ( main_byte == int('0x03',16) ):
            #print("Truck Completed")
            data_byte = canbus_byte[1:5]
            self.truck_completed(data_byte)
            return 1

        elif ( main_byte == int('0x04',16) ):
            #print("Product selected")
            data_byte   = canbus_byte[1]
            self.product_event(data_byte)
            return 0


        

