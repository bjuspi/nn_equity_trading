import os
import pandas as pd

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
rootdir = os.path.dirname(parentdir)
datadir = os.path.join(rootdir, "data")
interimdatadir = os.path.join(datadir, "interim")

daysforward = 5

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

        input_df = generate_input_file(price_df, fs_df)
        answer_df = generate_answer_file(input_df)
        
        destinationdir = os.path.join(os.path.join(datadir, "processed"), company)

        if not os.path.isdir(destinationdir):
            os.mkdir(destinationdir)
        
        input_df.to_csv(os.path.join(destinationdir, "input.txt"), header=False, sep="\t", index=False)
        input_df.to_csv(os.path.join(destinationdir, "input.csv"))

        answer_df.to_csv(os.path.join(destinationdir, "answer.txt"), header=False, sep="\t", index=False)
        answer_df.to_csv(os.path.join(destinationdir, "answer.csv"))

def generate_input_file(price_df, fs_df):
    return pd.merge_asof(price_df, fs_df, left_on="Dates", right_on="Financial release date")

def generate_answer_file(input_df):
    answer_df = input_df.copy()
    answer_df["next_price"] = answer_df["PX_OPEN"][daysforward:].reset_index(drop=True)
    answer_df = answer_df.dropna()
    answer_df["is_up"] = answer_df["next_price"] > answer_df["PX_OPEN"]
    return answer_df

if __name__ == "__main__":
    main() 