import util
util.load_saved_artifacts()
print(util.get_location_names())  # Should print a list of locations
print(util.get_estimated_price("Marathahalli", 1000, 2, 2))  # Replace "location_name" with a valid location