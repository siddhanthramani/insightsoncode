from datetime import datetime
from pytz import timezone
import pandas as pd

from helpers.helpers import convert_type
from constants.stringconstants import StringConstants
from constants.listconstants import ListConstants
from constants.dictconstants import DictConstants
from helpers.http_helpers import HttpRequests
from helpers.stack_helpers import InsightPointAutoStack

# this class is used to introduce points where time should be measured and allows us to view the result as a csv or dictionary
class InsightPoints(object):
    _IP_DICT_COLUMN_TYPES_DEFAULT = {"customer_id" : str, "project_id" : str, "node_id" : str, "branch_id" : str, "endpoint_id" : str, "code_id" : str}
    
    def __init__(self, project_id : str, dict_column_types : dict = _IP_DICT_COLUMN_TYPES_DEFAULT, project_timezone = "UTC", open_points_errors = "raise", **kwargs):
        self.sc_in_fastcode = StringConstants()
        self.lc_in_fastcode = ListConstants()
        self.dc_in_fastcode = DictConstants()
        
        # convert time zone as required
        self.project_timezone = project_timezone
        self.project_timezone_pytz = timezone(self.project_timezone)
        
        self.open_points_errors = open_points_errors

        # check if dict values are a string or list:
        for user_input_column_type in dict_column_types.values():
            if user_input_column_type not in self.lc_in_fastcode.list_acceptable_user_input_column_types:
                print(self.sc_in_fastcode.str_error_incorrect_user_defined_column_type.format(self.lc_in_fastcode.list_acceptable_user_input_column_types))
                raise TypeError

        self.dc_in_fastcode.add_dict_column_types(dict_column_types)
        self.lc_in_fastcode.add_list_column_names(list(dict_column_types.keys()))

        self.dict_fastcode = {}
        self.dict_fastcode[self.sc_in_fastcode.str_column_project_id] = convert_type(project_id, self.dc_in_fastcode.dict_column_types[self.sc_in_fastcode.str_column_project_id])
        
        list_constant_column_names = []
        for str_user_constant_column_name, user_constant_column_value in kwargs.items():
            if str_user_constant_column_name in self.lc_in_fastcode.list_user_column_names:
                self.dict_fastcode[str_user_constant_column_name] = convert_type(user_constant_column_value, self.dc_in_fastcode.dict_column_types[str_user_constant_column_name])
                list_constant_column_names.append(str_user_constant_column_name)
            else:
                print(self.sc_in_fastcode.str_note_unnecessary_input.format(str_user_constant_column_name))
        self.lc_in_fastcode.add_list_constant_column_names(list_constant_column_names)

    def log_startpoint(self, id : str,  **kwargs):
        # get the list of extra keys to let user know we won't be using them
        extra_keys = (set(kwargs.keys()) - set(self.lc_in_fastcode.list_user_column_names)) | (set(kwargs.keys()) & set(self.lc_in_fastcode.list_constant_column_names))
        if len(extra_keys) > 0:
            print(self.sc_in_fastcode.str_note_unnecessary_input.format(extra_keys))
            # removing extra keys
            for key in extra_keys:
                kwargs.pop(key)

        # get the list of blank keys to autofill with default values
        blank_keys = set(self.lc_in_fastcode.list_user_column_names) - (set(kwargs.keys()) | set(self.lc_in_fastcode.list_constant_column_names))
        for key in blank_keys:
            kwargs[key] = self.dc_in_fastcode.dict_column_types_default[key]
        
        # setting that start point's id value as user input
        self.dict_fastcode[id] = kwargs
        # calculating start point time
        self.dict_fastcode[id][self.sc_in_fastcode.str_column_start] = datetime.now(self.project_timezone_pytz)
        
        return self.dict_fastcode

    def log_stoppoint(self, id : str):
        # calculating end point time
        time_end = datetime.now(self.project_timezone_pytz)
        
        # checking if startpoint was defined. if yes, do calc. if not, default values if errortype default, else throw error
        self._error_handler_no_startpoint(id, time_end)

        return self.dict_fastcode

    def _error_handler_no_startpoint(self, id, time_end):
        try:
            self.dict_fastcode[id][self.sc_in_fastcode.str_column_stop] = time_end
            self.dict_fastcode[id][self.sc_in_fastcode.str_column_time_taken] = self.dict_fastcode[id][self.sc_in_fastcode.str_column_stop] - self.dict_fastcode[id][self.sc_in_fastcode.str_column_start]

            # converting to required_type
            self._convert_start_stop_timetaken(id)
        
        except KeyError as e:
            if self.open_points_errors in self.lc_in_fastcode.list_open_points_errors_raise:
                print(self.sc_in_fastcode.str_error_end_without_start)
                raise e
            elif self.open_points_errors in self.lc_in_fastcode.list_open_points_errors_default:
                self.dict_fastcode[id] = {}
                
                # get the list of user column names to autofill with default values
                blank_keys = set(self.lc_in_fastcode.list_user_column_names) - set(self.lc_in_fastcode.list_constant_column_names)
                for key in blank_keys:
                    self.dict_fastcode[id][key] = self.dc_in_fastcode.dict_column_types_default[key]
                
                self.dict_fastcode[id][self.sc_in_fastcode.str_column_start] = self.dc_in_fastcode.dict_column_types_default[self.sc_in_fastcode.str_column_start]
                self.dict_fastcode[id][self.sc_in_fastcode.str_column_time_taken] = self.dc_in_fastcode.dict_column_types_default[self.sc_in_fastcode.str_column_time_taken]
                self.dict_fastcode[id][self.sc_in_fastcode.str_column_stop] = time_end

                # converting to required_type
                self._convert_start_stop_timetaken(id)
            else:
                print(self.sc_in_fastcode.str_error_wrong_open_points_errors)
                raise e

    def _convert_start_stop_timetaken(self, id):
        if not self.dict_fastcode[id][self.sc_in_fastcode.str_column_start] == self.dc_in_fastcode.dict_column_types_default[self.sc_in_fastcode.str_column_start]:
            self.dict_fastcode[id][self.sc_in_fastcode.str_column_start] = self.dict_fastcode[id][self.sc_in_fastcode.str_column_start].strftime(self.sc_in_fastcode.str_date_time_format)
        if not self.dict_fastcode[id][self.sc_in_fastcode.str_column_stop] == self.dc_in_fastcode.dict_column_types_default[self.sc_in_fastcode.str_column_stop]:
            self.dict_fastcode[id][self.sc_in_fastcode.str_column_stop] = self.dict_fastcode[id][self.sc_in_fastcode.str_column_stop].strftime(self.sc_in_fastcode.str_date_time_format)
        if not self.dict_fastcode[id][self.sc_in_fastcode.str_column_time_taken] == self.dc_in_fastcode.dict_column_types_default[self.sc_in_fastcode.str_column_time_taken]:
            self.dict_fastcode[id][self.sc_in_fastcode.str_column_time_taken] = self.dict_fastcode[id][self.sc_in_fastcode.str_column_time_taken].total_seconds()

    def to_csv(self, filename, timestamp_required = 'y'):
        df_fastcode = self.to_dataframe()
        # adding timesteamp if required
        if timestamp_required.lower() in self.lc_in_fastcode.list_yes:
            filename += "_{}".format(datetime.now(self.project_timezone_pytz).strftime(self.sc_in_fastcode.str_date_time_format))
        
        # adding .csv if required and saving fastcode as csv
        if not filename.lower().endswith(".{}".format(self.sc_in_fastcode.str_csv)):
            filename = "{}.{}".format(filename, self.sc_in_fastcode.str_csv)
        df_fastcode.to_csv(filename)
    
    def to_dataframe(self):
        # removing and storing project_id, constant columns
        project_id = self.dict_fastcode.pop(self.sc_in_fastcode.str_column_project_id)
        dict_user_constant_column_names = {}
        for str_user_constant_column_name in set(self.lc_in_fastcode.list_constant_column_names):
            dict_user_constant_column_names[str_user_constant_column_name] = self.dict_fastcode.pop(str_user_constant_column_name)

        # checking if stoppoint was defined. if yes, do nothing. if not, default values if errortype default, else throw error
        self._error_handler_no_stoppoint()
        
        # creating dfs
        df_fastcode = pd.DataFrame(self.dict_fastcode).T
        # adding project id, constant columns
        df_fastcode[self.sc_in_fastcode.str_column_project_id] = project_id
        for str_user_constant_column_name, user_constant_column_value in dict_user_constant_column_names.items():
            df_fastcode[str_user_constant_column_name] = user_constant_column_value
        
        # reseting id as column 
        df_fastcode.index.name = self.sc_in_fastcode.str_column_id
        df_fastcode.reset_index()
        return df_fastcode

    def _error_handler_no_stoppoint(self):
        for key, val in self.dict_fastcode.items():
                try:
                    if val[self.sc_in_fastcode.str_column_stop]:
                        pass
                except KeyError as e:
                    if self.open_points_errors in self.lc_in_fastcode.list_open_points_errors_raise:
                        print(self.sc_in_fastcode.str_error_end_without_start)
                        raise e
                    elif self.open_points_errors in self.lc_in_fastcode.list_open_points_errors_default:
                        self.dict_fastcode[key][self.sc_in_fastcode.str_column_stop] = self.dc_in_fastcode.dict_column_types_default[self.sc_in_fastcode.str_column_stop]
                        self.dict_fastcode[key][self.sc_in_fastcode.str_column_time_taken] = self.dc_in_fastcode.dict_column_types_default[self.sc_in_fastcode.str_column_time_taken]
                        # converting to required_type
                        self._convert_start_stop_timetaken(key)
                    else:
                        print(self.sc_in_fastcode.str_error_wrong_open_points_errors)
                        raise e
    
    def log_send(self, api_key):
        dict_fastcode_temp = {}
        dict_fastcode_temp[self.sc_in_fastcode.str_column_project_id] = self.dict_fastcode.pop(self.sc_in_fastcode.str_column_project_id)
        for str_user_constant_column_name in set(self.lc_in_fastcode.list_constant_column_names):
            dict_fastcode_temp[str_user_constant_column_name] = self.dict_fastcode.pop(str_user_constant_column_name)
        
        # checking if endpoint was defined. if yes, do nothing. if not, default values if errortype default, else throw error
        self._error_handler_no_stoppoint()

        self.dict_fastcode[self.sc_in_fastcode.str_column_project_id] = dict_fastcode_temp[self.sc_in_fastcode.str_column_project_id]
        for str_user_constant_column_name in set(self.lc_in_fastcode.list_constant_column_names):
            self.dict_fastcode[str_user_constant_column_name] = dict_fastcode_temp[str_user_constant_column_name]

        HttpRequests().send_fastcode_results(api_key, self.dict_fastcode)