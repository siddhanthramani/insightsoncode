class StringConstants(object):
    
    def __init__(self):
        self.str_column_project_id = "project_id"
        self.str_column_id = "id"
        self.str_column_start = "start"
        self.str_column_end = "end"
        self.str_column_time_taken = "time_taken"
        self.str_column_cost = "cost"

        self.str_csv = "csv"

        self.str_date_time_format = "%Y-%m-%d_%H-%M-%S"

        self.str_error_end_without_start = "ERROR in code: END point called without START point"
        self.str_error_extra_keys = "ERROR in code: Extra keys have been passed and removing them"
        self.str_error_incorrect_type = "ERROR in code: {} is not of the correct type"