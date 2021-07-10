import os
import pandas as pd

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
rootdir = os.path.dirname(parentdir)
datadir = os.path.join(rootdir, "data")
interimdatadir = os.path.join(datadir, "interim")

def main():
    for root, subdirs, files in os.walk(interimdatadir):
        generate_processed_file(root, files)

def generate_processed_file(root, files):
    if ("price.csv" in files) and ("fs.csv" in files):
        company = os.path.basename(root)

        pricedir = os.path.join(os.path.join(interimdatadir, company), "price.csv")
        fsdir = os.path.join(os.path.join(interimdatadir, company), "fs.csv")

        price_df = pd.read_csv(pricedir, index_col=0)
        fs_df = pd.read_csv(fsdir, index_col=0)

        input_df = pd.merge_asof(price_df, fs_df, left_on="Dates", right_on="Financial release date")

        destinationdir = os.path.join(os.path.join(datadir, "processed"), company)

        if not os.path.isdir(destinationdir):
            os.mkdir(destinationdir)
        
        input_df.to_csv(os.path.join(destinationdir, "input.txt"), header=False, sep="\t", index=False)
        input_df.to_csv(os.path.join(destinationdir, "input.csv"))

if __name__ == "__main__":
    main() 