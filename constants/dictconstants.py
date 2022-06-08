from constants.stringconstants import StringConstants
sc_in_dc = StringConstants()

class DictConstants(object):
    def __init__(self):
        self.dict_column_types = {
            sc_in_dc.str_column_project_id : str,
            sc_in_dc.str_column_id : str,
            sc_in_dc.str_column_tags : str,
            sc_in_dc.str_column_start : float,
            sc_in_dc.str_column_end : float,
            sc_in_dc.str_column_time_taken : float,
            sc_in_dc.str_column_cost : float
        }
        # self.dict_column_types_default = {"l1_tag" : str(), "l2_tag" : str(), "l3_tag" : str(), "l4_tag" : str(), "l5_tag" : str(), "tags" : list()}
        self.dict_column_types_default = {
            sc_in_dc.str_column_project_id : str(),
            sc_in_dc.str_column_id : str(),
            sc_in_dc.str_column_tags : str(),
            sc_in_dc.str_column_start : float(),
            sc_in_dc.str_column_end : float(),
            sc_in_dc.str_column_time_taken : float(),
            sc_in_dc.str_column_cost : float()
        }

    def add_dict_column_types(self, dict_column_types : dict):
        self.dict_user_column_types = dict_column_types
        self.dict_user_column_types_default = dict(zip(dict_column_types.keys(), map(lambda const_type : const_type(), dict_column_types.values())))