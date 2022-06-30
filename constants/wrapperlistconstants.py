from constants.wrapperstringconstants import StringConstants

class ListConstants(object):
    
    def __init__(self):
        self.sc_in_lc = StringConstants()
        self.list_column_names = [
            self.sc_in_lc.str_column_customer_id,
            self.sc_in_lc.str_column_project_id,
            self.sc_in_lc.str_column_node_id,
            self.sc_in_lc.str_column_branch_id,
            self.sc_in_lc.str_column_endpoint_id,
            self.sc_in_lc.str_column_code_id,

            self.sc_in_lc.str_column_id, 
            self.sc_in_lc.str_column_start, 
            self.sc_in_lc.str_column_stop, 
            self.sc_in_lc.str_column_time_taken, 
            self.sc_in_lc.str_column_code_cost] 

        self.list_init_column_names = [
            self.sc_in_lc.str_column_customer_id,
            self.sc_in_lc.str_column_project_id,
            self.sc_in_lc.str_column_node_id,
            self.sc_in_lc.str_column_branch_id,
            self.sc_in_lc.str_column_endpoint_id]

        self.list_init_required_column_names = [
            self.sc_in_lc.str_column_project_id,
            self.sc_in_lc.str_column_endpoint_id]

        self.list_yes = ['y', 'yes']