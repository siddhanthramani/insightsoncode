from stringconstants import StringConstants
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
        # {"dict_column_types_default" : {"l1_tag" : str(), "l2_tag" : str(), "l3_tag" : str(), "l4_tag" : str(), "l5_tag" : str(), "tags" : list()}},
        self.dict_column_types_default = {
            sc_in_dc.str_column_project_id : str(),
            sc_in_dc.str_column_id : str(),
            sc_in_dc.str_column_tags : str(),
            sc_in_dc.str_column_start : float(),
            sc_in_dc.str_column_end : float(),
            sc_in_dc.str_column_time_taken : float(),
            sc_in_dc.str_column_cost : float()
        }

    def add_dict_constant_type(self, dict_constant):
        for dict_constant_key, dict_constant_value in dict_constant.items():
            if isinstance(dict_constant_value, dict):
                self.dict_constant_key = dict_constant_value
                self["{}_default".format(dict_constant_key)] = dict(zip(dict_constant_value.keys(), map(lambda const_type : const_type(), dict_constant_value.values()))) 
            else:
                print(sc_in_dc.str_error_incorrect_type.format(dict_constant_value))