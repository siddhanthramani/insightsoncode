from datetime import datetime
from h11 import Data
from pytz import timezone   
import pandas as pd
import json

# class fastcode_Constants()

str_column_project_id = "project_id"
str_column_start = "start"
str_column_end = "end"
str_column_time_taken = "time_taken"
str_column_cost = "cost"
str_column_id = "id"
str_csv = "csv"
str_date_time_format = "%Y-%m-%d_%H-%M-%S"
list_yes = ['y', 'yes']
list_column = ["l1_tag", "l2_tag", "l3_tag", "l4_tag", "l5_tag", "tags"]
str_column_tags = "tags"
dict_id_type = {'id' : str}

dict_column_types_default = {"l1_tag" : str(), "l2_tag" : str(), "l3_tag" : str(), "l4_tag" : str(), "l5_tag" : str(), "tags" : list()}
dict_column_types_default = {
    str_column_start : float(),
    str_column_end : float(),
    str_column_time_taken : float(),
    str_column_cost : float()
}


def convert_type(var, var_type):
    return var_type(var)

def convert_typ_pd_series(df, col, col_type):
    df[col] = df[col].astype(col_type)


class InsightPoints(object):
    
    def __init__(self, project_id, creds, timezone = "UTC"):
        self.project_timezone = timezone
        self.project_timezone_pytz = timezone(self.project_timezone)
        
        self.dict_fastcode = {}
        self.dict_fastcode[str_column_project_id] = project_id

    def start_point(self, id,  **kwargs):
        # main_tag = "code1", sub_tag= "bq"
        blank_keys = set(list_column) - set(kwargs.keys())
        extra_keys = set(kwargs.keys()) - set(list_column)
        if len(extra_keys) > 0:
            print("{} : {}".format(str_error_extra_keys, extra_keys))
        
        for key in blank_keys:
            kwargs[key] = dict_column_types_default[key]
        
        id = convert_type(id, dict_id_type[str_column_id])
        self.dict_fastcode[id] = kwargs

        s = datetime.now(self.project_timezone_pytz)
        self.dict_fastcode[id][str_column_start] = s
        
        return self.dict_fastcode

    def end_point(self, id = ""):
        e = datetime.now(self.project_timezone_pytz)
        self.dict_fastcode[id][str_column_end] = e
        try:
            self.dict_fastcode[id][str_column_time_taken] = self.dict_fastcode[id][str_column_end] - self.dict_fastcode[id][str_column_start]
        except:
            print(str_error_end_without_start)
            self.dict_fastcode[id][str_column_start] = dict_column_types_default[dict_column_types_default]
            self.dict_fastcode[id][str_column_time_taken] = dict_column_types_default[str_column_time_taken]
        
        return self.dict_fastcode

    def fastcode_csv(self, filename, timestamp = 'n'):
        project_id = self.dict_fastcode.pop(str_column_project_id)
        
        for key, val in self.dict_fastcode.items():
                try:
                    if val[str_column_end]:
                        pass
                except:
                    self.dict_fastcode[key][str_column_end] = dict_column_types_default[str_column_end]
                    self.dict_fastcode[key][str_column_time_taken] = dict_column_types_default[str_column_time_taken]
        
        df_fastcode = pd.DataFrame(self.dict_fastcode).T
        df_fastcode[str_column_project_id] = project_id
        df_fastcode.index.name = str_column_id
        df_fastcode.reset_index()
        
        if timestamp.lower() in list_yes:
            timestamp += "_{}".format(datetime.now(self.project_timezone_pytz).strftime(str_date_time_format))
        if filename.lower().endswith(".{}".format(str_csv)):
            df_fastcode.to_csv(filename)
        else:
            df_fastcode.to_csv("{}.{}".format(filename, str_csv))

    def log_fastcode(project_id, creds):
        pass
        # check into bq and log details


class InsightsonCode(object):
    
    def __init__(self, filename):
        self.filename = filename        
        data = pd.read_csv(self.filename)
        data[str_column_id] = data[str_column_id].astype(str)
        self.data = data

    def include_cost(self, jsonname):
        with open(jsonname, 'r') as myfile:
            cost_data = myfile.read()
        dict_id_cost_map = json.loads(cost_data)
        self.data[str_column_cost] = list(map(lambda id : dict_id_cost_map.get(id, dict_column_types_default[str_column_cost]), self.data[str_column_id]))

        return self.data

def aggregate(self, level = [], filters = {}, time_span = [], cols_to_agg = [str_column_time_taken], aggs = ["avg"]):

    for filter_key, filter_vals in filters.items():
        if filter_key is str_column_tags:
            data = data[list(map(lambda x : len(set(x).intersection(set(filter_vals))) > 0, data[filter_key]))]
        else:
            data = data[data[filter_key].isin(filter_vals)]

    level += time_span
    data.groupby(level).agg({cols_to_agg : aggs})

    return data
# include_cost("filename.csv", "cost.json")
aggregate("filename_sample.csv - Sheet2.csv", level = ["l1_tag", "l2_tag"], filters = {"l2_tag" : ["al", "bl"], "tags" : ["e", "d"]}, time_span = {}, cols_to_agg = [str_column_time_taken, str_column_cost], aggs = ["avg", "sum"])