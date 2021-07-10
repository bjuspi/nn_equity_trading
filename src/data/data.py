import os
import re
import pandas as pd

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
rootdir = os.path.dirname(parentdir)
datadir = os.path.join(rootdir, "data")
rawdatadir = os.path.join(datadir, "raw")

for root, subdirs, files in os.walk(rawdatadir):
    print('--\nroot = ' + root)
    print(subdirs)
    print(files)

    if "price.xlsx" in files:
        company = os.path.basename(root)

        df = pd.read_excel(os.path.join(root, "price.xlsx"))
        
        header = df.iloc[0]
        df = df[1:]
        df.columns = header
        df["Dates"] = df.index

        df.to_csv(os.path.join(os.path.join(os.path.join(datadir, "interim"), company), "price.csv"))