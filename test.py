import loadrite_3180_class as lr3180
import my_test_canbus_bytes as test_canbus
json_file = "data_loadrite.json"

my_test_dict = test_canbus.package_bytes
loadrite = lr3180.loadrite_class()
loadrite.upload_self_data(json_file)
#lr3180.print_dictionary(loadrite.dictionary)

print(f" \n-------------------------------\n")
for key in my_test_dict.keys():
    new_array = my_test_dict[key]
    a = loadrite.get_action(new_array)
    if (a == 1):
        lr3180.print_dictionary(loadrite.dictionary)