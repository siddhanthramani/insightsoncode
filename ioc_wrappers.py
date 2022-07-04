from datetime import datetime
from pytz import timezone
from functools import wraps
import pandas as pd
import os.path

from helpers.helpers import convert_type
from constants.wrapperstringconstants import StringConstants
from constants.wrapperlistconstants import ListConstants
from constants.wrapperdictconstants import DictConstants
from helpers.http_helpers import HttpRequests
from helpers.stack_helpers import InsightPointAutoStack

sc_in_fastcode_wrappers = StringConstants()

def _log_ids(ioc_ids : dict, log_ids, kwargs_log_ids):
    ioc_prepend = sc_in_fastcode_wrappers.str_insights_on_code_prepend
    to_remove_kwargs_log_ids_keys = []

    for kwargs_log_ids_key, kwargs_log_ids_value in kwargs_log_ids.items():
        if ioc_ids.get(kwargs_log_ids_key, 0):
            to_remove_kwargs_log_ids_keys += [kwargs_log_ids_key]
            if ioc_prepend:
                kwargs_log_ids_key = kwargs_log_ids_key.split(ioc_prepend)[1]
            log_ids[kwargs_log_ids_key] = kwargs_log_ids_value
            
    for key in to_remove_kwargs_log_ids_keys:
        kwargs_log_ids.pop(key)
    
    return log_ids, kwargs_log_ids


def log_constantpoints(api_key : str, csv_filename : str, mode : str = 'a', timestamp_required : str = 'n', project_timezone : str = "UTC", **log_ids):
    def log_endpoint(endpoint_id : str = ''):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                sc_in_log_endpoint = StringConstants()
                dc_in_log_endpoint = DictConstants()
                
                log_ids[sc_in_log_endpoint.str_column_endpoint_id] = endpoint_id
                appended_log_ids, removed_kwargs = _log_ids(dc_in_log_endpoint.dict_init_ids, log_ids, kwargs)
                
                ipw = InsightPointsWrapper(api_key, project_timezone, **appended_log_ids)
                result = func(ipw, *args, **removed_kwargs)
                
                ipw.to_csv(csv_filename, mode, timestamp_required)
                
                return result
            return wrapper
        return decorator
    return log_endpoint

def log_codepoint(code_id : str = '', **code_logs):
    def decorator_main(func):
        @wraps(func)
        def wrapper(ipw, *args, **kwargs):
            sc_in_log_codepoint = StringConstants()
            dc_in_log_codepoint = DictConstants()
            
            code_logs[sc_in_log_codepoint.str_column_code_id] = code_id
            appended_log_ids, removed_kwargs = _log_ids(dc_in_log_codepoint.dict_codepoint_ids, code_logs, kwargs)
            
            ipw.log_startpoint(**appended_log_ids)
            result = func(ipw, *args, **removed_kwargs)
            ipw.log_stoppoint()
            
            return result
        return wrapper
    return decorator_main

class InsightPointsWrapper(object):
    _DICT_COLUMN_TYPES = {"customer_id" : str, "project_id" : str, "node_id" : str, "branch_id" : str, "endpoint_id" : str, "code_id" : str}
    
    def __init__(self, api_key : str, project_timezone : str = "UTC", **log_ids):
        self.api_key = api_key
        self._create_required_objects()
        self._change_timezone(project_timezone)
        self._check_if_compulsory_logs_are_present(log_ids, self.lc_in_fastcode.list_init_compulsory_column_names)
        log_ids = self._check_extra_logs(log_ids, self.lc_in_fastcode.list_init_column_names)
        log_ids = self._check_blank_logs(log_ids, self.lc_in_fastcode.list_init_column_names)
        log_ids = self._force_convert_log_to_required_format(log_ids)
        self.dict_fastcode = log_ids

    def _force_convert_log_to_required_format(self, logs):
        for log_key, log_value in logs.items():
            logs[log_key] = convert_type(log_value, self.dc_in_fastcode.dict_column_types.get(log_key))

        return logs

    def _check_if_compulsory_logs_are_present(self, log_ids, compulsory_logs_list):
        for required_column in compulsory_logs_list:
            if not log_ids.get(required_column, 0):
                print(self.sc_in_fastcode.str_error_required_columns_not_present.format(self.lc_in_fastcode.list_init_compulsory_column_names))
                raise Exception
        
    def _check_extra_logs(self, log_ids, required_logs_list):
        extra_keys = set(log_ids.keys()) - set(required_logs_list)
        if len(extra_keys) > 0:
            print(self.sc_in_fastcode.str_note_unnecessary_input.format(extra_keys))
            # removing extra keys
            for key in extra_keys:
                log_ids.pop(key)
        return log_ids

    def _check_blank_logs(self, log_ids, required_logs_list):
        # get the list of blank keys to autofill with default values
        blank_keys = set(required_logs_list) - set(log_ids.keys())
        for key in blank_keys:
            log_ids[key] = self.dc_in_fastcode.dict_column_types_default[key]
        return log_ids

    def _change_timezone(self, project_timezone):
        self.project_timezone = project_timezone
        self.project_timezone_pytz = timezone(self.project_timezone)

    def _create_required_objects(self):
        self.sc_in_fastcode = StringConstants()
        self.lc_in_fastcode = ListConstants()
        self.dc_in_fastcode = DictConstants()
        self.autostack = InsightPointAutoStack()

    def add_constant_logs(self, **const_logs):
        const_logs = self._check_extra_logs(const_logs, self.lc_in_fastcode.list_constant_column_names)
        const_logs = self._force_convert_log_to_required_format(const_logs)
        for const_log_name, const_log_value in const_logs.items():
            self.dict_fastcode[const_log_name] = const_log_value

    def add_endpoint_logs(self, **endpoint_logs):
        endpoint_logs = self._check_extra_logs(endpoint_logs, self.lc_in_fastcode.list_endpoint_column_names)
        endpoint_logs = self._force_convert_log_to_required_format(endpoint_logs)
        for endpoint_log_name, endpoint_log_value in endpoint_logs.items():
            self.dict_fastcode[endpoint_log_name] = endpoint_log_value

    def add_code_logs(self, **code_logs):
        code_logs = self._check_extra_logs(code_logs, self.lc_in_fastcode.list_code_column_names)
        code_logs = self._force_convert_log_to_required_format(code_logs)
        for code_log_name, code_log_value in code_logs.items():
            self.dict_fastcode[self.id][code_log_name] = code_log_value
            
    # def add_logs(self, **log_ids):
    #     log_ids = self._check_extra_ids(log_ids, self.lc_in_fastcode.list_init_column_names)
    #     log_ids = self._force_convert_log_ids_to_string(log_ids)
    #     for log_id_name, log_id_value in log_ids.items():
    #         self.dict_fastcode[log_id_name] = log_id_value
    
    def log_startpoint(self, **code_logs):
        self._check_if_compulsory_logs_are_present(code_logs, self.lc_in_fastcode.list_code_compulsory_column_names)
        code_logs = self._check_extra_logs(code_logs, self.lc_in_fastcode.list_code_column_names)
        code_logs = self._check_blank_logs(code_logs, self.lc_in_fastcode.list_code_column_names)
        code_logs = self._force_convert_log_to_required_format(code_logs)
        
        # id is required to map startpoints and respective endpoint.
        id = self.autostack.push()
        self.id = id
        self.dict_fastcode[id] = {}

        for code_log_key, code_log_value in code_logs.items():
            self.dict_fastcode[id][code_log_key] = code_log_value
        
        self.dict_fastcode[id][self.sc_in_fastcode.str_column_start] = datetime.now(self.project_timezone_pytz)

    def log_stoppoint(self):
        # popping value of stack to set id
        id = self.autostack.pop()
        self.id = id
        # calculating stop point time
        self.dict_fastcode[id][self.sc_in_fastcode.str_column_stop] = datetime.now(self.project_timezone_pytz)
        self.dict_fastcode[id][self.sc_in_fastcode.str_column_time_taken] = self.dict_fastcode[id][self.sc_in_fastcode.str_column_stop] - self.dict_fastcode[id][self.sc_in_fastcode.str_column_start]
        self._convert_start_stop_timetaken(id)

    def _convert_start_stop_timetaken(self, id):
        self.dict_fastcode[id][self.sc_in_fastcode.str_column_start] = self.dict_fastcode[id][self.sc_in_fastcode.str_column_start].strftime(self.sc_in_fastcode.str_date_time_format)
        self.dict_fastcode[id][self.sc_in_fastcode.str_column_stop] = self.dict_fastcode[id][self.sc_in_fastcode.str_column_stop].strftime(self.sc_in_fastcode.str_date_time_format)
        self.dict_fastcode[id][self.sc_in_fastcode.str_column_time_taken] = self.dict_fastcode[id][self.sc_in_fastcode.str_column_time_taken].total_seconds()

    def to_dataframe(self):
        dict_user_constant_column_names = {}
        for str_user_constant_column_name in set(self.lc_in_fastcode.list_init_column_names):
            dict_user_constant_column_names[str_user_constant_column_name] = self.dict_fastcode.pop(str_user_constant_column_name)

        # creating dfs
        self.df_fastcode = pd.DataFrame(self.dict_fastcode).T
       
        for str_user_constant_column_name, user_constant_column_value in dict_user_constant_column_names.items():
            self.df_fastcode[str_user_constant_column_name] = user_constant_column_value

        return self.df_fastcode

    def to_csv(self, csv_filename, mode = 'a', timestamp_required = 'n'):
        self.to_dataframe()
        # adding timesteamp if required
        if timestamp_required.lower() in self.lc_in_fastcode.list_yes:
            csv_filename += self.sc_in_fastcode.str_append_string.format(datetime.now(self.project_timezone_pytz).strftime(self.sc_in_fastcode.str_date_time_format))

        # adding .csv if required and saving fastcode as csv
        if not csv_filename.lower().endswith(self.sc_in_fastcode.str_append_file_format.format(self.sc_in_fastcode.str_csv)):
            csv_filename = self.sc_in_fastcode.str_filename_with_extension.format(csv_filename, self.sc_in_fastcode.str_csv)
        
        # check if csv already exists to know whether or not to include header info
        if os.path.isfile(csv_filename):     
            self.df_fastcode.sort_index(axis=1).to_csv(csv_filename, mode = mode, header = False)
        else:
            self.df_fastcode.sort_index(axis=1).to_csv(csv_filename, mode = mode)

    def log_send(self):
        try: 
            self.autostack.pop()
            print(self.sc_in_fastcode.str_error_log_send_startend_mismatch)
            raise Exception
        except:
            pass

        HttpRequests().send_fastcode_results(self.api_key, self.dict_fastcode)