from datetime import datetime
from h11 import Data
from pytz import timezone
import pandas as pd
import json

from helpers.helpers import convert_type, convert_type_pd_series
from constants.stringconstants import StringConstants
from constants.listconstants import ListConstants
from constants.dictconstants import DictConstants
sc_in_fastcode = StringConstants()
lc_in_fastcode = ListConstants()
dc_in_fastcode = DictConstants()


class InsightPoints(object):
    
    def __init__(self, project_id, dict_column_types = {"l1_tag" : str, "l2_tag" : str, "l3_tag" : str, "l4_tag" : str, "l5_tag" : str, "tags" : list}, project_timezone = "UTC"):
        self.project_timezone = project_timezone
        self.project_timezone_pytz = timezone(self.project_timezone)
        
        dc_in_fastcode.add_dict_column_types(dict_column_types)
        lc_in_fastcode.add_list_column_names(list(dict_column_types.keys()))

        self.dict_fastcode = {}
        self.dict_fastcode[sc_in_fastcode.str_column_project_id] = project_id
        return self.dict_fastcode

    def start_point(self, id,  **kwargs):
        blank_keys = set(lc_in_fastcode.list_column_names) - set(kwargs.keys())
        extra_keys = set(kwargs.keys()) - set(lc_in_fastcode.list_column_names)
        if len(extra_keys) > 0:
            print("{} : {}".format(sc_in_fastcode.str_error_extra_keys, extra_keys))
        for key in blank_keys:
            kwargs[key] = dc_in_fastcode.dict_column_types_default[key]
        
        id = convert_type(id, dc_in_fastcode.dict_column_types[sc_in_fastcode.str_column_id])
        self.dict_fastcode[id] = kwargs

        time_start = datetime.now(self.project_timezone_pytz)
        self.dict_fastcode[id][sc_in_fastcode.str_column_start] = time_start
        return self.dict_fastcode

    def end_point(self, id = ""):
        time_end = datetime.now(self.project_timezone_pytz)
        self.dict_fastcode[id][sc_in_fastcode.str_column_end] = time_end
        try:
            self.dict_fastcode[id][sc_in_fastcode.str_column_time_taken] = self.dict_fastcode[id][sc_in_fastcode.str_column_end] - self.dict_fastcode[id][sc_in_fastcode.str_column_start]
        except:
            print(sc_in_fastcode.str_error_end_without_start)
            self.dict_fastcode[id][sc_in_fastcode.str_column_start] = dc_in_fastcode.dict_column_types_default[sc_in_fastcode.str_column_start]
            self.dict_fastcode[id][sc_in_fastcode.str_column_time_taken] = dc_in_fastcode.dict_column_types_default[sc_in_fastcode.str_column_time_taken]
        return self.dict_fastcode

    def fastcode_csv(self, filename, timestamp = 'y'):
        project_id = self.dict_fastcode.pop(sc_in_fastcode.str_column_project_id)
        
        for key, val in self.dict_fastcode.items():
                try:
                    if val[sc_in_fastcode.str_column_end]:
                        pass
                except:
                    self.dict_fastcode[key][sc_in_fastcode.str_column_end] = dc_in_fastcode.dict_column_types_default[sc_in_fastcode.str_column_end]
                    self.dict_fastcode[key][sc_in_fastcode.str_column_time_taken] = dc_in_fastcode.dict_column_types_default[sc_in_fastcode.str_column_time_taken]
        
        df_fastcode = pd.DataFrame(self.dict_fastcode).T
        df_fastcode[sc_in_fastcode.str_column_project_id] = project_id
        df_fastcode.index.name = sc_in_fastcode.str_column_id
        df_fastcode.reset_index()
        
        if timestamp.lower() in lc_in_fastcode.list_yes:
            timestamp += "_{}".format(datetime.now(self.project_timezone_pytz).strftime(sc_in_fastcode.str_date_time_format))
        if filename.lower().endswith(".{}".format(sc_in_fastcode.str_csv)):
            df_fastcode.to_csv(filename)
        else:
            df_fastcode.to_csv("{}.{}".format(filename, sc_in_fastcode.str_csv))


class InsightsonCode(object):
    
    def __init__(self, filename):
        self.filename = filename
        data = pd.read_csv(self.filename)
        data[sc_in_fastcode.str_column_id] = data[sc_in_fastcode.str_column_id].astype(str)
        self.data = data

    def include_cost(self, jsonname):
        with open(jsonname, 'r') as myfile:
            cost_data = myfile.read()
        dict_id_cost_map = json.loads(cost_data)
        self.data[sc_in_fastcode.str_column_cost] = list(map(lambda id : dict_id_cost_map.get(id, dc_in_fastcode.dict_column_types_default[sc_in_fastcode.str_column_cost]), self.data[sc_in_fastcode.str_column_id]))
        return self.data

    def aggregate(self, level = [], filters = {}, time_span = [], cols_to_agg = [sc_in_fastcode.str_column_time_taken], aggs = ["avg"]):

        for filter_key, filter_vals in filters.items():
            if filter_key is sc_in_fastcode.str_column_tags:
                data = data[list(map(lambda x : len(set(x).intersection(set(filter_vals))) > 0, data[filter_key]))]
            else:
                data = data[data[filter_key].isin(filter_vals)]

        level += time_span
        data.groupby(level).agg({cols_to_agg : aggs})
        return data



# include_cost("filename.csv", "cost.json")
# aggregate("filename_sample.csv - Sheet2.csv", level = ["l1_tag", "l2_tag"], filters = {"l2_tag" : ["al", "bl"], "tags" : ["e", "d"]}, time_span = {}, cols_to_agg = [sc_in_fastcode.str_column_time_taken, sc_in_fastcode.str_column_cost], aggs = ["avg", "sum"])