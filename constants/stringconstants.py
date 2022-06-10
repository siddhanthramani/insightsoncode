class StringConstants(object):
    
    def __init__(self):
        self.str_column_project_id = "project_id"
        self.str_column_id = "id"
        self.str_column_start = "start"
        self.str_column_end = "end"
        self.str_column_time_taken = "time_taken"
        self.str_column_cost = "cost"

        self.str_csv = "csv"
        self.str_json = "json"

        self.avg = "avg"
        self.mean = "mean"

        self.str_date_time_format = "%Y-%m-%d_%H-%M-%S"

        self.str_error_wrong_open_points_errors = "ERROR in code : Wrong ope_points_errors value"
        self.str_error_end_without_start = "ERROR in code: END point called without START point"
        self.str_error_extra_keys = "ERROR in code: Extra keys have been passed and removing them"
        self.str_error_incorrect_type = "ERROR in code: {} is not of the correct type"
        self.str_error_helper_pd_convert_type = "ERROR in code: Column list and column type list lengths are not matching"