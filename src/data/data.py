import os
import pandas as pd

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
rootdir = os.path.dirname(parentdir)

df = pd.read_excel(rootdir + r"\data\raw\AMZN\price.xlsx")

header = df.iloc[0]
df = df[1:]
df.columns = header
df["Dates"] = df.index

df.to_csv(rootdir + r"\data\interim\AMZN\price.csv")