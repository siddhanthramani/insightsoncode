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

    def include_cost_columns(self, jsonname):
        # # adding .json if required and reading json into dataframe
        if not jsonname.lower().endswith(".{}".format(sc_in_fastcode_analytics.str_json)):
            jsonname = "{}.{}".format(jsonname, sc_in_fastcode_analytics.str_json)
        with open(jsonname, 'r') as myfile:
            cost_data = myfile.read()
        dict_id_cost_map = json.loads(cost_data)

        # mapping using id column and loading cost data to data
        self.data[sc_in_fastcode_analytics.str_column_cost] = list(map(lambda id : dict_id_cost_map.get(id, dc_in_fastcode_analytics.dict_column_types_default[sc_in_fastcode_analytics.str_column_cost]), self.data[sc_in_fastcode_analytics.str_column_id]))
        return self.data

    def include_groupby_datetime_columns(self, column_end : str = sc_in_fastcode_analytics.str_column_end, column_end_string_format : str = sc_in_fastcode_analytics.str_date_time_format, h = 1, d = 1, w = 1, m = 1, y =1):
        temp_end_column = self.data[column_end].copy()
        temp_end_column = pd.to_datetime(temp_end_column, format = column_end_string_format)
        if y == 1:
            self.data[sc_in_fastcode_analytics.str_column_hour] = temp_end_column.dt.to_period(sc_in_fastcode_analytics.str_to_period__frequency_year).map(str)
        if m == 1:
            self.data[sc_in_fastcode_analytics.str_column_hour] = temp_end_column.dt.to_period(sc_in_fastcode_analytics.str_to_period__frequency_month).map(str)
        if w == 1:
            self.data[sc_in_fastcode_analytics.str_column_hour] = temp_end_column.dt.to_period(sc_in_fastcode_analytics.str_to_period__frequency_week).map(str)
        if d == 1:
            self.data[sc_in_fastcode_analytics.str_column_hour] = temp_end_column.dt.to_period(sc_in_fastcode_analytics.str_to_period__frequency_day).map(str)
        if h == 1:
            self.data[sc_in_fastcode_analytics.str_column_hour] = temp_end_column.dt.to_period(sc_in_fastcode_analytics.str_to_period__frequency_hour).map(str)
        return self.data

    def aggregate(self, level = [], filters = {}, time_span = [], cols_to_agg = [sc_in_fastcode_analytics.str_column_time_taken], aggs = ["avg"]):
        self.agg_data = self.data.copy()
        for filter_key, filter_vals in filters.items():
            if isinstance(dc_in_fastcode_analytics.dict_column_types_default[filter_key], list):
                self.agg_data = self.agg_data[list(map(lambda x : len(set(x).intersection(set(filter_vals))) > 0, self.agg_data[filter_key]))]
            else:
                self.agg_data = self.agg_data[self.agg_data[filter_key].isin(filter_vals)]

        # changing avg to mean for aggregation
        if sc_in_fastcode_analytics.avg in aggs:
            aggs = list(map(lambda x: x.replace(sc_in_fastcode_analytics.avg, sc_in_fastcode_analytics.mean),aggs))
        # adding time_span to level
        level += time_span
        # creating agg_dict to pass to groupby.agg
        agg_dict = dict()
        for col_to_agg in cols_to_agg:
            agg_dict[col_to_agg] = aggs
        self.agg_data = self.agg_data.groupby(level).agg(agg_dict)
        self.agg_data = self.agg_data.reset_index()
        return self.agg_data