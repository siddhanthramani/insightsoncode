from time import sleep
from fastcode import InsightPoints as ip
fc = ip(project_id = "1", creds = "creds1")
# fc.start_fastcode(project_id = "1", creds = "creds1")

fc.start_point(id = "1",  main_tag = "code1", sub_tag= "bq", tags = [])
a = [1, 2]
sleep(1)
# fc.end_point( id = "1")

fc.start_point(id = "2",  main_tag = "code1", sub_tag= "pg", tags = [])
b = [3, 9]
sleep(0.9)

fc.start_point( id = "4",  main_tag = "code1", sub_tag= "pg", tags = [])
b = [3, 9]
sleep(0.7)
fc.end_point( id = "4")



fc.start_point( id = "3",  main_tag = "code1", sub_tag= "pg", tags = [])
b = [3, 9]
sleep(0.7)
fc.end_point( id = "3")

fc.end_point( id = "2")

fc.fastcode_csv("filename")