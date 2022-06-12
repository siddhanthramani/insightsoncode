from constants.stringconstants import StringConstants
sc_in_lc = StringConstants()

class ListConstants(object):
    
    def __init__(self):
        self.list_yes = ['y', 'yes']
        self.list_open_points_errors_raise = ['r', 'raise']
        self.list_open_points_errors_default = ['d', 'default']
        self.list_ioc_column_names = [
            sc_in_lc.str_column_project_id, 
            sc_in_lc.str_column_id, 
            sc_in_lc.str_column_start, 
            sc_in_lc.str_column_end, 
            sc_in_lc.str_column_time_taken, 
            sc_in_lc.str_column_cost] 
        
        self.list_user_input_column_names = [
            sc_in_lc.str_column_project_id,
            sc_in_lc.str_column_id]

        self.list_column_names = self.list_ioc_column_names.copy()
        
    def add_list_column_names(self, list_column_names : list):
        self.list_user_column_names = list_column_names

        self.list_column_names += self.list_user_column_names
        self.list_user_input_column_names += self.list_user_column_names