from datetime import datetime
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

# this class is used to introduce points where time should be measured and allows us to view the result as a csv or dictionary
class InsightPoints(object):
    
    def __init__(self, project_id : str, dict_column_types  : dict = {"l1_tag" : str, "l2_tag" : str, "l3_tag" : str, "l4_tag" : str, "l5_tag" : str, "tags" : list}, project_timezone = "UTC", open_points_errors = "raise"):
        self.project_timezone = project_timezone
        self.project_timezone_pytz = timezone(self.project_timezone)
        
        self.open_points_errors = open_points_errors

        dc_in_fastcode.add_dict_column_types(dict_column_types)
        lc_in_fastcode.add_list_column_names(list(dict_column_types.keys()))
        
        self.dict_fastcode = {}
        self.dict_fastcode[sc_in_fastcode.str_column_project_id] = convert_type(project_id, dc_in_fastcode.dict_column_types[sc_in_fastcode.str_column_project_id])

    def start_point(self, id : str,  **kwargs):
        # get the list of extra keys to let user know we won't be using them
        extra_keys = set(kwargs.keys()) - set(lc_in_fastcode.list_user_column_names)
        if len(extra_keys) > 0:
            print("{} : {}".format(sc_in_fastcode.str_error_extra_keys, extra_keys))
            # removing extra keys
            for key in extra_keys:
                kwargs.pop(key)

        # get the list of blank keys to autofill with default values
        blank_keys = set(lc_in_fastcode.list_user_column_names) - set(kwargs.keys())
        for key in blank_keys:
            kwargs[key] = dc_in_fastcode.dict_column_types_default[key]
        
        # setting that start point's id value as user input
        self.dict_fastcode[id] = kwargs
        # calculating start point time
        self.dict_fastcode[id][sc_in_fastcode.str_column_start] = datetime.now(self.project_timezone_pytz)
        
        return self.dict_fastcode

    def end_point(self, id : str):
        # calculating end point time
        time_end = datetime.now(self.project_timezone_pytz)

        # checking if startpoint was defined. if yes, do calc. if not, default values if errortype default, else throw error
        self.error_handler_no_startpoint(id, time_end)

        return self.dict_fastcode

    def error_handler_no_startpoint(self, id, time_end):
        try:
            self.dict_fastcode[id][sc_in_fastcode.str_column_end] = time_end
            self.dict_fastcode[id][sc_in_fastcode.str_column_time_taken] = self.dict_fastcode[id][sc_in_fastcode.str_column_end] - self.dict_fastcode[id][sc_in_fastcode.str_column_start]
        except KeyError as e:
            if self.open_points_errors in lc_in_fastcode.list_open_points_errors_raise:
                print(sc_in_fastcode.str_error_end_without_start)
                raise e
            elif self.open_points_errors in lc_in_fastcode.list_open_points_errors_default:
                self.dict_fastcode[id] = {}
                
                # get the list of user column names to autofill with default values
                blank_keys = set(lc_in_fastcode.list_user_column_names)
                for key in blank_keys:
                    self.dict_fastcode[id][key] = dc_in_fastcode.dict_column_types_default[key]
                
                self.dict_fastcode[id][sc_in_fastcode.str_column_start] = dc_in_fastcode.dict_column_types_default[sc_in_fastcode.str_column_start]
                self.dict_fastcode[id][sc_in_fastcode.str_column_time_taken] = dc_in_fastcode.dict_column_types_default[sc_in_fastcode.str_column_time_taken]
                self.dict_fastcode[id][sc_in_fastcode.str_column_end] = time_end
            else:
                print(sc_in_fastcode.str_error_wrong_open_points_errors)
                raise e

    def fastcode_csv(self, filename, timestamp_required = 'y'):
        # removing and storing project_id
        project_id = self.dict_fastcode.pop(sc_in_fastcode.str_column_project_id)
        
        # checking if endpoint was defined. if yes, do nothing. if not, default values if errortype default, else throw error
        self.error_handler_no_endpoint_fastcode_csv()
                    
        # creating dfs, reseting id as column 
        df_fastcode = pd.DataFrame(self.dict_fastcode).T
        df_fastcode[sc_in_fastcode.str_column_project_id] = project_id
        df_fastcode.index.name = sc_in_fastcode.str_column_id
        df_fastcode.reset_index()
        
        # adding timesteamp if required
        if timestamp_required.lower() in lc_in_fastcode.list_yes:
            filename += "_{}".format(datetime.now(self.project_timezone_pytz).strftime(sc_in_fastcode.str_date_time_format))
        
        # adding .csv if required and saving fastcode as csv
        if not filename.lower().endswith(".{}".format(sc_in_fastcode.str_csv)):
            filename = "{}.{}".format(filename, sc_in_fastcode.str_csv)
        df_fastcode.to_csv(filename)

    def error_handler_no_endpoint_fastcode_csv(self):
        for key, val in self.dict_fastcode.items():
                try:
                    if val[sc_in_fastcode.str_column_end]:
                        pass
                except KeyError as e:
                    if self.open_points_errors in lc_in_fastcode.list_open_points_errors_raise:
                        print(sc_in_fastcode.str_error_end_without_start)
                        raise e
                    elif self.open_points_errors in lc_in_fastcode.list_open_points_errors_default:
                        self.dict_fastcode[key][sc_in_fastcode.str_column_end] = dc_in_fastcode.dict_column_types_default[sc_in_fastcode.str_column_end]
                        self.dict_fastcode[key][sc_in_fastcode.str_column_time_taken] = dc_in_fastcode.dict_column_types_default[sc_in_fastcode.str_column_time_taken]
                    else:
                        print(sc_in_fastcode.str_error_wrong_open_points_errors)
                        raise e

# this class is used to analyse our measured data and derive insights out of it
class InsightsonCode(object):
    
    def __init__(self, filename):
        self.filename = filename
        # adding .csv if required and reading csv into dataframe
        if not self.filename.lower().endswith(".{}".format(sc_in_fastcode.str_csv)):
            self.filename = "{}.{}".format(self.filename, sc_in_fastcode.str_csv)
        data = pd.read_csv(self.filename)
        
        # id should be a string. So ensuring type is maintained by explicity converting id to string
        data = convert_type_pd_series(data, sc_in_fastcode.str_column_id, dc_in_fastcode.dict_column_types[sc_in_fastcode.str_column_id])
        
        self.data = data
        return self.data

    def include_cost(self, jsonname):
        # # adding .json if required and reading json into dataframe
        if not jsonname.lower().endswith(".{}".format(sc_in_fastcode.str_json)):
            jsonname = "{}.{}".format(self.filename, sc_in_fastcode.str_json)
        with open(jsonname, 'r') as myfile:
            cost_data = myfile.read()
        dict_id_cost_map = json.loads(cost_data)

        # mapping using id column and loading cost data to data
        self.data[sc_in_fastcode.str_column_cost] = list(map(lambda id : dict_id_cost_map.get(id, dc_in_fastcode.dict_column_types_default[sc_in_fastcode.str_column_cost]), self.data[sc_in_fastcode.str_column_id]))
        return self.data

    def aggregate(self, level = [], filters = {}, time_span = [], cols_to_agg = [sc_in_fastcode.str_column_time_taken], aggs = ["avg"]):

        for filter_key, filter_vals in filters.items():
            if isinstance(dc_in_fastcode.dict_column_types_default[sc_in_fastcode[filter_key]], list):
                data = data[list(map(lambda x : len(set(x).intersection(set(filter_vals))) > 0, data[filter_key]))]
            else:
                data = data[data[filter_key].isin(filter_vals)]

        level += time_span
        data.groupby(level).agg({cols_to_agg : aggs})
        return data



# include_cost("filename.csv", "cost.json")
# aggregate("filename_sample.csv - Sheet2.csv", level = ["l1_tag", "l2_tag"], filters = {"l2_tag" : ["al", "bl"], "tags" : ["e", "d"]}, time_span = {}, cols_to_agg = [sc_in_fastcode.str_column_time_taken, sc_in_fastcode.str_column_cost], aggs = ["avg", "sum"])