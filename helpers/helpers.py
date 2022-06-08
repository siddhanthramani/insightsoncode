def convert_type(var, var_type):
    return var_type(var)

def convert_type_pd_series(df, col, col_type):
    df[col] = df[col].astype(col_type)