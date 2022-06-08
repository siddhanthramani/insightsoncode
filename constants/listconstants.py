from stringconstants import StringConstants
sc_in_lc = StringConstants()
class ListConstants(object):
    
    def __init__(self):
        self.list_yes = ['y', 'yes']
    def add_list_column_names(self, list_column_names : list):
        self.list_user_column_names = list_column_names