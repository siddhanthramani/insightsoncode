import pandas as pd
import json

from helpers.helpers import convert_type_pd_series
from constants.stringconstants import StringConstants
from constants.listconstants import ListConstants
from constants.dictconstants import DictConstants

sc_in_fastcode_analytics = StringConstants()
lc_in_fastcode_analytics = ListConstants()
dc_in_fastcode_analytics = DictConstants()

# this class is used to analyse our measured data and derive insights out of it
class InsightsonCode(object):
    
    def __init__(self, filename, dict_column_types  : dict = {"l1_tag" : str, "l2_tag" : str, "l3_tag" : str, "l4_tag" : str, "l5_tag" : str, "tags" : list}):
        self.filename = filename
        # adding .csv if required and reading csv into dataframe
        if not self.filename.lower().endswith(".{}".format(sc_in_fastcode_analytics.str_csv)):
            self.filename = "{}.{}".format(self.filename, sc_in_fastcode_analytics.str_csv)
        data = pd.read_csv(self.filename)
        
        dc_in_fastcode_analytics.add_dict_column_types(dict_column_types)
        lc_in_fastcode_analytics.add_list_column_names(list(dict_column_types.keys()))

        # id should be a string. So ensuring type is maintained by explicity converting id to string
        data = convert_type_pd_series(data, 
        [sc_in_fastcode_analytics.str_column_project_id, sc_in_fastcode_analytics.str_column_id], 
        [
        dc_in_fastcode_analytics.dict_column_types[sc_in_fastcode_analytics.str_column_project_id], 
        dc_in_fastcode_analytics.dict_column_types[sc_in_fastcode_analytics.str_column_id]
        ])
        
        self.data = data

    def include_cost(self, jsonname):
        # # adding .json if required and reading json into dataframe
        if not jsonname.lower().endswith(".{}".format(sc_in_fastcode_analytics.str_json)):
            jsonname = "{}.{}".format(jsonname, sc_in_fastcode_analytics.str_json)
        with open(jsonname, 'r') as myfile:
            cost_data = myfile.read()
        dict_id_cost_map = json.loads(cost_data)

        # mapping using id column and loading cost data to data
        self.data[sc_in_fastcode_analytics.str_column_cost] = list(map(lambda id : dict_id_cost_map.get(id, dc_in_fastcode_analytics.dict_column_types_default[sc_in_fastcode_analytics.str_column_cost]), self.data[sc_in_fastcode_analytics.str_column_id]))
        return self.data

    def aggregate(self, level = [], filters = {}, time_span = [], cols_to_agg = [sc_in_fastcode_analytics.str_column_time_taken], aggs = ["avg"]):

        for filter_key, filter_vals in filters.items():
            if isinstance(dc_in_fastcode_analytics.dict_column_types_default[filter_key], list):
                self.data = self.data[list(map(lambda x : len(set(x).intersection(set(filter_vals))) > 0, self.data[filter_key]))]
            else:
                self.data = self.data[self.data[filter_key].isin(filter_vals)]

        # changing avg to mean for aggregation
        if sc_in_fastcode_analytics.avg in aggs:
            aggs = list(map(lambda x: x.replace(sc_in_fastcode_analytics.avg, sc_in_fastcode_analytics.mean),aggs))
        # adding time_span to level
        level += time_span
        # creating agg_dict to pass to groupby.agg
        agg_dict = dict()
        for col_to_agg in cols_to_agg:
            agg_dict[col_to_agg] = aggs
        self.data = self.data.groupby(level).agg(agg_dict)
        self.data = self.data.reset_index()
        return self.data

# include_cost("filename.csv", "cost.json")
# aggregate("filename_sample.csv - Sheet2.csv", level = ["l1_tag", "l2_tag"], filters = {"l2_tag" : ["al", "bl"], "tags" : ["e", "d"]}, time_span = {}, cols_to_agg = [sc_in_fastcode_analytics.str_column_time_taken, sc_in_fastcode_analytics.str_column_cost], aggs = ["avg", "sum"])