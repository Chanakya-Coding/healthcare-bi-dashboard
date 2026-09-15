import pandas as pd

df = pd.read_csv(r'C:\Users\cnara\Desktop\Projects\healthcare-bi-pipeline\data\raw\diabetic_data.csv')

print(df.shape)
print(df.head())
print(df.info())