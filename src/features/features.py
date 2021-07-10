import os
import pandas as pd

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
rootdir = os.path.dirname(parentdir)
datadir = os.path.join(rootdir, "data")
interimdatadir = os.path.join(datadir, "interim")

days_forward = 5
price_gap = 2
reference_price = "PX_OPEN"

def main():
    for root, subdirs, files in os.walk(interimdatadir):
        generate_processed_file(root, files)

def generate_processed_file(root, files):
    if "price.csv" in files:
        company = os.path.basename(root)

        pricedir = os.path.join(os.path.join(interimdatadir, company), "price.csv")
        price_df = pd.read_csv(pricedir, index_col=0)

        answer_df = generate_answer_file(price_df)

        destinationdir = os.path.join(os.path.join(datadir, "processed"), company)

        if not os.path.isdir(destinationdir):
            os.mkdir(destinationdir)

        answer_df.to_csv(os.path.join(destinationdir, "answer.txt"), header=False, sep="\t", index=False)
        answer_df.to_csv(os.path.join(destinationdir, "answer.csv"))
        
        if "fs.csv" in files:
            fsdir = os.path.join(os.path.join(interimdatadir, company), "fs.csv")
            fs_df = pd.read_csv(fsdir, index_col=0)

            input_df = generate_input_file(price_df, fs_df)
            
            input_df.to_csv(os.path.join(destinationdir, "input.txt"), header=False, sep="\t", index=False)
            input_df.to_csv(os.path.join(destinationdir, "input.csv"))

def generate_input_file(price_df, fs_df):
    return pd.merge_asof(price_df, fs_df, left_on="Dates", right_on="Financial release date")

def generate_answer_file(price_df):
    answer_df = price_df.copy()
    answer_df["next_price"] = answer_df[reference_price][days_forward:].reset_index(drop=True)
    answer_df = answer_df.dropna()
    answer_df["is_up"] = answer_df["next_price"] > answer_df[reference_price] + price_gap
    return answer_df

if __name__ == "__main__":
    main() 