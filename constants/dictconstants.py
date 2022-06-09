from constants.stringconstants import StringConstants
from helpers.helpers import merge_two_dicts
sc_in_dc = StringConstants()

class DictConstants(object):
    def __init__(self):
        self.dict_ioc_column_types = {
            sc_in_dc.str_column_project_id : str,
            sc_in_dc.str_column_id : str,
            sc_in_dc.str_column_start : float,
            sc_in_dc.str_column_end : float,
            sc_in_dc.str_column_time_taken : float,
            sc_in_dc.str_column_cost : float
        }
        # self.dict_column_types_default = {"l1_tag" : str(), "l2_tag" : str(), "l3_tag" : str(), "l4_tag" : str(), "l5_tag" : str(), "tags" : list()}
        self.dict_ioc_column_types_default = {
            sc_in_dc.str_column_project_id : str(),
            sc_in_dc.str_column_id : str(),
            sc_in_dc.str_column_start : float(),
            sc_in_dc.str_column_end : float(),
            sc_in_dc.str_column_time_taken : float(),
            sc_in_dc.str_column_cost : float()
        }
        self.dict_user_input_column_types = {
            sc_in_dc.str_column_project_id : str
            ,sc_in_dc.str_column_id : str}

        self.dict_user_input_column_types_default = {
            sc_in_dc.str_column_project_id : str()
            ,sc_in_dc.str_column_id : str()
            }

        self.dict_column_types = self.dict_ioc_column_types.copy()
        self.dict_column_types_default = self.dict_ioc_column_types_default.copy()

    def add_dict_column_types(self, dict_column_types : dict):
        self.dict_user_column_types = dict_column_types
        self.dict_user_column_types_default = dict(zip(dict_column_types.keys(), map(lambda const_type : const_type(), dict_column_types.values())))
        
        self.dict_column_types = merge_two_dicts(self.dict_column_types, self.dict_user_column_types)
        self.dict_column_types_default = merge_two_dicts(self.dict_column_types_default, self.dict_user_column_types_default)
        
        self.dict_user_input_column_types = merge_two_dicts(self.dict_user_input_column_types, self.dict_user_column_types)
        self.dict_user_input_column_types_default = merge_two_dicts(self.dict_user_input_column_types_default, self.dict_user_column_types_default)