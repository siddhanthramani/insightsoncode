from constants.stringconstants import StringConstants

class ListConstants(object):
    
    def __init__(self):
        self.sc_in_lc = StringConstants()
        self.list_yes = ['y', 'yes']
        self.list_acceptable_user_input_column_types = [str, list]
        self.list_open_points_errors_raise = ['r', 'raise']
        self.list_open_points_errors_default = ['d', 'default']
        self.list_ioc_column_names = [
            self.sc_in_lc.str_column_project_id, 
            self.sc_in_lc.str_column_id, 
            self.sc_in_lc.str_column_start, 
            self.sc_in_lc.str_column_stop, 
            self.sc_in_lc.str_column_time_taken, 
            self.sc_in_lc.str_column_cost] 
        
        self.list_user_input_column_names = [
            self.sc_in_lc.str_column_project_id,
            self.sc_in_lc.str_column_id]

        self.list_column_names = self.list_ioc_column_names.copy()
        
        # defining default if user does not input any values
        self.list_user_column_names = []
        self.list_constant_column_names = []

    def add_list_column_names(self, list_column_names : list):
        self.list_user_column_names = list_column_names

        self.list_column_names += self.list_user_column_names
        self.list_user_input_column_names += self.list_user_column_names

    def add_list_constant_column_names(self, list_constant_column_names : list):
        self.list_constant_column_names = list_constant_column_names