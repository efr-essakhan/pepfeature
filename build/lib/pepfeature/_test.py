"""
    *** A private module ***

    A Test:
    To check the veracity of the results produced from the feature calculation algorithms of this package.
    The test consists of code that first generates peptide features on Sample_Data.csv and compares each value of the output DataFrame with a Model Dataframe (Model_Data.csv) for accuracy.

    Usage:
        If pepfeature module is imported than call pepfeature._test.execute() in script
        Results of test will be displayed in console

"""

import pandas as pd
import pepfeature as pep
import pkg_resources

def execute(Ncores=4):
    sample = pkg_resources.resource_filename('pepfeature', 'data/Sample_Data.csv')
    model = pkg_resources.resource_filename('pepfeature', "data/Model_Data.csv")

    sample_df = pd.read_csv(sample)
    model_df = pd.read_csv(model)

    r = 10
    sample_df = sample_df.loc[range(r)]
    model_df = model_df.loc[range(r)]

    # Calculating all features
    sample_df = pep.aa_all_feat.calc_df(dataframe=sample_df, k=2, Ncores=Ncores)

    # #Removing AA sequuence column from each
    del sample_df['Info_window_seq']
    del model_df['Info_window_seq']

    matched = []
    unmatched = []

    for idx, column in enumerate(model_df):
        for model_val, sample_val in zip(model_df[column], sample_df[column]):
            model_val = round(float(model_val), 3)
            sample_val = round(float(sample_val), 3)

            if model_val == sample_val:
                # print(f'{model_val} == {sample_val} ------- Model: {column}')
                matched.append(str(column))

            else:
                print(f'Model: {model_val} =/= Sample: {sample_val} ------- Model: {column}')
                unmatched.append(str(column))  # will be used to compare the columns that don't mathch with each other

    print('____________________________________________________')
    print('Result of test:')
    print('____________________________________________________')

    y = []
    [y.append(i) for i in matched if i not in y]  # Removing duplicates
    print(f'{len(y)} Matched features. Names of matched features:')
    print(y)

    print('____________________________________________________')

    x = []
    [x.append(i) for i in unmatched if i not in x]  # Removing duplicates

    print(f'{len(x)} Umatched features.')
    if len(x) == 0:
        print(f'100% accurate results produced by this package.')
    else:
        print(f'Names of unmathced features: {x}')










####################################
# def _check_invalid_aa_existance_in_dataframe(df):
#
#     bad_aa = 0
#     bad_aa_seq = []
#     ####First Check if model dataframe even contains invalid amino acid sequences
#     for index, row in df.iterrows():
#         seq = row['Info_window_seq']
#
#         for c in 'BJXZ':
#
#             if c in seq:
#                 bad_aa += 1
#                 bad_aa_seq.append(seq)
#                 print(f'{seq} ------- For char: {c}')
#             else:
#                 print(f'{c} NOT IN {seq}')
#
#     print(bad_aa)
