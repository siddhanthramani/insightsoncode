from time import sleep
from fastcode import InsightPoints as ip

# Create InsightPoints object at the entry point of Code
fc = ip(project_id = "1"
        , dict_column_types = {"client_id" : str, "code_id" : str}
        , project_timezone = "UTC")

# create a startpoint and pass required paramters
fc.log_startpoint(id = "1",  client_id = "1", code_id = "a")
sleep(0.6)
# close the startpoint by calling endpoint and having the same ID
fc.log_endpoint(id = "1")

# similar example
fc.log_startpoint(id = "2",  client_id = "1", code_id = "a")
sleep(0.7)
fc.log_endpoint(id = "2")

# similar example
fc.log_startpoint(id = "3",  client_id = "1", code_id = "b")
sleep(0.8)
fc.log_endpoint(id = "3")

# save the file to a csv at the end of the code
fc.to_dataframe("filename")