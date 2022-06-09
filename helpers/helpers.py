def convert_type(var, var_type):
    return var_type(var)

def convert_type_pd_series(df, col, col_type):
    df[col] = df[col].astype(col_type)
    return df

def merge_two_dicts(dict_1, dict_2):
    dict_out = dict_1.copy()
    dict_out.update(dict_2)
    return dict_out