import pandas
import json

class ClientSeparetor:
    def __init__(self, dataframe):
        self.df = dataframe

    
    
    def data_by_client_name(self):

        with open(r"C:\Users\jimmy\source\Python Projects\Company Statistics\client_name_mappings.json", 'r',  encoding="utf8") as file:
            
            name_dict = json.load(file)

            self.df["Client Name"] = self.df["ΚΛΗΘΕΙΣ ΑΡΙΘΜΟΣ"].astype(str).replace(name_dict)

            # Drop rows where "Client Name" still contains numbers
            self.df = self.df[~self.df["Client Name"].str.contains(r'\d')]
            return self.df
        
        
        