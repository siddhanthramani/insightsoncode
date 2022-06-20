from constants.wrapperstringconstants import StringConstants

class DictConstants(object):
    def __init__(self):
        self.sc_in_dc = StringConstants()

        self.dict_column_types = {
            self.sc_in_dc.str_column_customer_id : str,
            self.sc_in_dc.str_column_project_id : str,
            self.sc_in_dc.str_column_node_id : str,
            self.sc_in_dc.str_column_branch_id : str,
            self.sc_in_dc.str_column_endpoint_id : str,
            self.sc_in_dc.str_column_code_id : str,

            self.sc_in_dc.str_column_id : str,
            self.sc_in_dc.str_column_start : str,
            self.sc_in_dc.str_column_stop : str,
            self.sc_in_dc.str_column_time_taken : float,
            self.sc_in_dc.str_column_cost : float
        }
        # self.dict_column_types_default = {"l1_tag" : str(), "l2_tag" : str(), "l3_tag" : str(), "l4_tag" : str(), "l5_tag" : str(), "tags" : list()}
        self.dict_column_types_default = {
            self.sc_in_dc.str_column_customer_id : str(),
            self.sc_in_dc.str_column_project_id : str(),
            self.sc_in_dc.str_column_node_id : str(),
            self.sc_in_dc.str_column_branch_id : str(),
            self.sc_in_dc.str_column_endpoint_id : str(),
            self.sc_in_dc.str_column_code_id : str(),

            self.sc_in_dc.str_column_id : str(),
            self.sc_in_dc.str_column_start : str(),
            self.sc_in_dc.str_column_stop : str(),
            self.sc_in_dc.str_column_time_taken : float(),
            self.sc_in_dc.str_column_cost : float()
        }