from datetime import datetime
from pytz import timezone
from functools import wraps

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
            
            kwargs_log_ids_key = kwargs_log_ids_key.split(ioc_prepend)[1]
            log_ids[kwargs_log_ids_key] = kwargs_log_ids_value
            
    for key in to_remove_kwargs_log_ids_keys:
        kwargs_log_ids.pop(key)
    
    return log_ids, kwargs_log_ids


def log_constantpoints(api_key : str, project_timezone : str = "UTC", log_send = 0, **log_ids):
    def log_endpoint(endpoint_id : str = ''):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                sc_in_log_endpoint = StringConstants()
                dc_in_log_endpoint = DictConstants()
                
                log_ids[sc_in_log_endpoint.str_column_endpoint_id] = endpoint_id
                appended_log_ids, removed_kwargs = _log_ids(dc_in_log_endpoint.dict_endpoint_ids, log_ids, kwargs)
                
                ipw = InsightPointsWrapper(api_key, project_timezone, **appended_log_ids)
                result = func(ipw, *args, **removed_kwargs)
                if log_send == 1:
                    ipw.log_send()
                else:
                    print(vars(ipw))
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
        self._check_if_required_ids_are_present(log_ids)
        log_ids = self._check_extra_ids(log_ids)
        log_ids = self._check_blank_ids(log_ids)
        self.dict_fastcode = self._force_convert_log_ids_to_string(log_ids)
    
    def _force_convert_log_ids_to_string(self, log_ids):
        log_ids = dict(zip(log_ids.keys(), list(map(str, log_ids.values()))))
        return log_ids

    def _check_if_required_ids_are_present(self, log_ids):
        for required_column in self.lc_in_fastcode.list_init_required_column_names:
            if not log_ids.get(required_column, 0):
                print(self.sc_in_fastcode.str_error_required_columns_not_present.format(self.lc_in_fastcode.list_init_required_column_names))
                raise Exception
        
    def _check_extra_ids(self, log_ids):
        extra_keys = set(log_ids.keys()) - set(self.lc_in_fastcode.list_init_column_names)
        if len(extra_keys) > 0:
            print(self.sc_in_fastcode.str_note_unnecessary_input.format(extra_keys))
            # removing extra keys
            for key in extra_keys:
                log_ids.pop(key)
        return log_ids

    def _check_blank_ids(self, log_ids):
        # get the list of blank keys to autofill with default values
        blank_keys = set(self.lc_in_fastcode.list_init_column_names) - set(log_ids.keys())
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

    def add_ids(self, **log_ids):
        log_ids = self._check_extra_ids(log_ids)
        log_ids = self._force_convert_log_ids_to_string(log_ids)
        for log_id_name, log_id_value in log_ids.items():
            self.dict_fastcode[log_id_name] = log_id_value
    
    def log_startpoint(self, **code_logs):
        if not code_logs[self.sc_in_fastcode.str_column_code_id]:
            print(self.sc_in_fastcode.str_error_required_columns_not_present.format(self.sc_in_fastcode.str_column_code_id))
            raise Exception
        else:
            code_id = convert_type(code_logs[self.sc_in_fastcode.str_column_code_id], self.dc_in_fastcode.dict_column_types[self.sc_in_fastcode.str_column_code_id])
        # setting that start point's id value as user
        id = self.autostack.push()
        self.dict_fastcode[id] = {}
        self.dict_fastcode[id][self.sc_in_fastcode.str_column_code_id] = code_id
        # calculating start point time
        self.dict_fastcode[id][self.sc_in_fastcode.str_column_start] = datetime.now(self.project_timezone_pytz)

    def log_stoppoint(self):
        # popping value of stack to set id
        id = self.autostack.pop()
        # calculating stop point time
        self.dict_fastcode[id][self.sc_in_fastcode.str_column_stop] = datetime.now(self.project_timezone_pytz)
        self.dict_fastcode[id][self.sc_in_fastcode.str_column_time_taken] = self.dict_fastcode[id][self.sc_in_fastcode.str_column_stop] - self.dict_fastcode[id][self.sc_in_fastcode.str_column_start]
        self._convert_start_stop_timetaken(id)

    def _convert_start_stop_timetaken(self, id):
        self.dict_fastcode[id][self.sc_in_fastcode.str_column_start] = self.dict_fastcode[id][self.sc_in_fastcode.str_column_start].strftime(self.sc_in_fastcode.str_date_time_format)
        self.dict_fastcode[id][self.sc_in_fastcode.str_column_stop] = self.dict_fastcode[id][self.sc_in_fastcode.str_column_stop].strftime(self.sc_in_fastcode.str_date_time_format)
        self.dict_fastcode[id][self.sc_in_fastcode.str_column_time_taken] = self.dict_fastcode[id][self.sc_in_fastcode.str_column_time_taken].total_seconds()

    def log_send(self):
        try: 
            self.autostack.pop()
            print(self.sc_in_fastcode.str_error_log_send_startend_mismatch)
            raise Exception
        except:
            pass

        HttpRequests().send_fastcode_results(self.api_key, self.dict_fastcode)