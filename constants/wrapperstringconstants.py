class StringConstants(object):
    
    def __init__(self):
        
        self.str_column_id = "id"
        self.str_column_start = "start"
        self.str_column_stop = "stop"
        self.str_column_time_taken = "time_taken"
        self.str_column_code_cost = "code_cost"
        
        # ensure there is underscore at the end of code prepend
        self.str_insights_on_code_prepend = ""
        self.str_column_customer_id = "customer_id"
        self.str_column_project_id = "project_id"
        self.str_column_node_id = "node_id"
        self.str_column_branch_id = "branch_id"
        self.str_column_endpoint_id = "endpoint_id"
        self.str_column_code_id = "code_id"

        self.str_column_second = "second"
        self.str_column_minute = "minute"
        self.str_column_hour = "hour"
        self.str_column_day = "day"
        self.str_column_week = "week"
        self.str_column_month = "month"

        self.str_to_period__frequency_year = "Y"
        self.str_to_period__frequency_month = "M"
        self.str_to_period__frequency_week = "W"
        self.str_to_period__frequency_day = "D"
        self.str_to_period__frequency_hour = "H"

        self.str_csv = "csv"
        self.str_json = "json"
        self.str_filename_with_extension = "{}.{}"
        self.str_append_string = "_{}"
        self.str_append_file_format = ".{}"
        
        self.avg = "avg"
        self.mean = "mean"

        self.str_date_time_format = "%Y-%m-%d_%H-%M-%S"

        

        self.str_note_unnecessary_input = "NOTE: Unnecessary input, ignoring it - {}"
        self.str_error_required_columns_not_present = "ERROR IN CODE : {} is/are required entry"

        self.str_error_wrong_open_points_errors = "ERROR in code: Wrong open_points_errors value"
        self.str_error_end_without_start = "ERROR in code: END point called without START point"
        self.str_error_incorrect_type = "ERROR in code: {} is not of the correct type"
        self.str_error_helper_pd_convert_type = "ERROR in code: Column list and column type list lengths are not matching"
        self.str_error_incorrect_user_defined_column_type = "ERROR in code: Acceptable dict_column_types are {}"
        self.str_error_log_send_startend_mismatch = "ERROR IN CODE : Insightpoints startpoint and endpoint mismatch"
        