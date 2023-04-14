# append dis_symp.csv and dbmi_disease_symptoms.csv to mayo_disease_data.csv

import pandas as pd

# read the three CSV files into pandas dataframes
mayo_df = pd.read_csv("mayo_disease_data.csv")
dis_symp_df = pd.read_csv("disease_symptoms_wiki.csv")
dbmi_df = pd.read_csv("dbmi_disease_symptoms.csv")

# concatenate the dataframes vertically
combined_df = pd.concat([mayo_df, dis_symp_df, dbmi_df], ignore_index=True)

# save the combined dataframe to a new CSV file
combined_df.to_csv("combined_data.csv", index=False)


