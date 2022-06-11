import pandas as pd
import glob, os

def merge_csvs(path_of_files, concated_file_name):
    
    os.chdir(path_of_files)
    i_file = 0
    final_file = pd.DataFrame()
    for file in glob.glob("*.csv"):
        if i_file == 0:
            final_file = pd.read_csv(file)  
            i_file = 1
        else:
            final_file = pd.concat([final_file, pd.read_csv(file)])
    
    final_file.to_csv(concated_file_name)
    return final_file

