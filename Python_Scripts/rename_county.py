import itertools
import pandas as pd

df = pd.read_csv("NJ_EV_output_grouped.csv")

for i in range(len(df['County'])):
    df['County'][i] = df['County'][i].replace("County", "")
    df['County'][i] = df['County'][i].strip()
    df['County'][i] = df['County'][i].lower()

df.to_csv('NJ_EV_output_grouped.csv', index=False)