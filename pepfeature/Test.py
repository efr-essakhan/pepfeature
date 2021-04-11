import pepfeature
import pandas as pd
import time
import pepfeature as pep
import string

sample_df = pd.read_csv('Sample_Data.csv')
model_df = pd.read_csv("Model_Data.csv")



def check_invalid_aa_existance(df):
    #This was ran over Model_Dataset and no invalid AA were found

    bad_aa = 0
    bad_aa_seq = []
    ####First Check if model dataframe even contains invalid amino acid sequences
    for index, row in df.iterrows():
        seq = row['Info_window_seq']

        for c in 'BJXZ':

            if c in seq:
                bad_aa += 1
                bad_aa_seq.append(seq)
                print(f'{seq} ------- For char: {c}')

    print(bad_aa)



if __name__ == '__main__':
   # pep.all_features.calc_csv(dataframe=sample_df, k=2, Ncores=4)

    sample_df = sample_df.loc[range(2)]
    model_df = model_df.loc[range(2)]


    #Calculating all features
    sample_df = pep.all_features.calc_df(dataframe=sample_df, k=2, Ncores=4)

    #Removing AA sequuence column from each
    del sample_df['Info_window_seq']
    del model_df['Info_window_seq']


    matched = 0
    unmatched = []

    for idx, column in enumerate(model_df):
        for sample_val, model_val in zip(model_df[column], sample_df[column]):
            model_val = round(float(model_val), 3)
            sample_val = round(float(sample_val), 3)

            if model_val == sample_val:
                print(f'{model_val} == {sample_val}')
                matched += 1

            else:
                print(
                    f'{model_val} NOT {sample_val} ------- Model: {column}')
                unmatched.append(column)  # will be used to compare the columns that don't mathch with each other

    print('____________________________________________________')
    print(f'matched: {matched}')

    print(f'unmatched: {len(unmatched)}')

















