from stringconstants import StringConstants
sc_in_dc = StringConstants()

class DefaultConstants(object):
    def __init__(self) -> None:
        dict_column_types_default = {"l1_tag" : str(), "l2_tag" : str(), "l3_tag" : str(), "l4_tag" : str(), "l5_tag" : str(), "tags" : list()}
        dict_column_types_default = {
            sc_in_dc.str_column_start : float(),
            sc_in_dc.str_column_end : float(),
            sc_in_dc.str_column_time_taken : float(),
            sc_in_dc.str_column_cost : float()
        }