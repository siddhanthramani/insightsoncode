from constants.stringconstants import StringConstants
sc_in_helpers = StringConstants()

def convert_type(var, var_type):
    return var_type(var)

def convert_type_pd_series(df, list_cols, list_col_types):
    if len(list_cols) == len(list_col_types):
        for col_index in range(len(list_cols)):
            df[list_cols[col_index]] = df[list_cols[col_index]].astype(list_col_types[col_index])
    else:
        print(sc_in_helpers.str_error_helper_pd_convert_type)

    return df

def merge_two_dicts(dict_1, dict_2):
    dict_out = dict_1.copy()
    dict_out.update(dict_2)
    return dict_out

