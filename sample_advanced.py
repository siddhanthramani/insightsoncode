from time import sleep
from fastcode import InsightPoints as ip

# Create InsightPoints object at the entry point of Code
fc = ip(project_id = "1"
        , dict_column_types = {"client_id" : str, "branch_id" : str, "api_id" : str, "function_id" : str, "code_id" : str, "importance_and_isactive_tag" : list}
        , project_timezone = "UTC")

# Create a startpoint for the entire code. Give it a unqiue ID and fill the required parameters. 
# Only client and branch id parameters are filled to understand how the entire code performs.
fc.log_startpoint(id = "1",  client_id = "client1", branch_id= "dev", tags = ["notimp", "active"])

# test random functions are defined for testing
def random_function_1():
    sleep(0.1)
def random_function_2():
    sleep(0.2)

# a test random api which calls random function 1
def random_api():
    sleep(0.1)

    # Create a startpoint for the random function. Give it a unqiue ID and fill the required parameters.
    fc.log_startpoint(id = "3",  client_id = "client1", branch_id= "dev", api_id = "1", function_id = "1")
    random_function_1()
    # Close the started point by calling endpoint with correct id
    fc.log_endpoint( id = "3")

# Create a startpoint for the random function. Give it a unqiue ID and fill the required parameters.
fc.log_startpoint(id = "2",  client_id = "client1", branch_id= "dev", api_id = "1")
random_api()
fc.log_endpoint( id = "2")
# Create a startpoint for the random function. Give it a unqiue ID and fill the required parameters.

fc.log_startpoint(id = "4",  client_id = "client1", branch_id= "dev", function_id = "2")
random_function_2()
# Close the started point by calling endpoint with correct id
fc.log_endpoint( id = "4")

# Close the first started point
fc.log_endpoint( id = "1")

# save the file to a csv at the end of the code
fc.to_dataframe("filename", timestamp_required = 'n')