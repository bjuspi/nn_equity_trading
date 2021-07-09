import os, sys
import pandas as pd

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
rootdir = os.path.dirname(parentdir)

y = r"\data\raw\AMZN\price.xlsx"
pricedir = rootdir + y
x = pd.read_excel(pricedir)

print("hello")