import pandas as pd

df = pd.read_csv('data/exel/nature.csv')
column_data = df.iloc[:, 6]
column_data.to_csv('output_file.txt', index=False, header=False)
