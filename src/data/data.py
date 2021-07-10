import os
import numpy as np
import pandas as pd

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
rootdir = os.path.dirname(parentdir)
datadir = os.path.join(rootdir, "data")
rawdatadir = os.path.join(datadir, "raw")

reference_date = np.datetime64("2013-03-31")

def main():
    for root, subdirs, files in os.walk(rawdatadir):
        generate_interim_files(root, files)

def generate_interim_files(root, files):
    if "price.xlsx" in files:
        generate_price_interim_file(root)

    if "fs.xlsx" in files: 
        generate_financial_statement_interim_file(root)

def generate_price_interim_file(root):
    company = os.path.basename(root)

    price_df = pd.read_excel(os.path.join(root, "price.xlsx"), header=1)
    price_df["Dates"] = (price_df["Dates"] - reference_date).dt.days
    
    destinationdir = os.path.join(os.path.join(datadir, "interim"), company)

    if not os.path.isdir(destinationdir):
        os.mkdir(destinationdir)

    price_df.to_csv(os.path.join(destinationdir, "price.txt"), header=False, sep="\t", index=False)
    price_df.to_csv(os.path.join(destinationdir, "price.csv"))

def generate_financial_statement_interim_file(root):
    company = os.path.basename(root)

    if not company == "FB":
        return
    
    fs_df = pd.read_excel(os.path.join(root, "fs.xlsx"), sheet_name="transpose complete")
    fs_df["Financial release date"] = (fs_df["Financial release date"] - reference_date).dt.days
    fs_df["Financial Date"] = (fs_df["Financial Date"] - reference_date).dt.days
    
    destinationdir = os.path.join(os.path.join(datadir, "interim"), company)    
    
    if not os.path.isdir(destinationdir):
        os.mkdir(destinationdir)
    
    fs_df.to_csv(os.path.join(destinationdir, "fs.txt"), header=False, sep="\t", index=False)
    fs_df.to_csv(os.path.join(destinationdir, "fs.csv"))

if __name__ == "__main__":
    main() 