import pandas as pd
import pepfeature as pep
import timeit
import statistics

if __name__ == '__main__':
    cores_to_use = 4
    times_to_run = 3

    mysetup = '''
import pepfeature as pep
import pandas as pd

rows_10 = pd.read_csv('10_seq.csv')
rows_50 = pd.read_csv('50_seq.csv')
rows_100 = pd.read_csv('100_seq.csv')
rows_500 = pd.read_csv('500_seq.csv')
rows_1000 = pd.read_csv('1000_seq.csv')

    '''

    print(f'Running code x{times_to_run} with {cores_to_use} core multiprocessing...\n')

    csv_names = ['10_seq.csv', '50_seq.csv', '100_seq.csv', '500_seq.csv', '1000_seq.csv']

    for idx,csv in enumerate(["rows_10", "rows_50", "rows_100", "rows_500", "rows_1000" ]):
        statement = f"pep.aa_all_feat.calc_df(dataframe={csv}, aa_column='Info_window_seq', Ncores={cores_to_use}, k=2)"
        resutls = timeit.repeat(stmt=statement, setup=mysetup, repeat = times_to_run, number = 1, globals = None)
        print(f"{csv_names[idx]}    min {min(resutls)} s , mean {statistics.mean(resutls)} s , max {max(resutls)} s")


# def create_subset_datasets():
#
#
#     # Creating CSV's of 10,50,100,500,1000 peptides
#
#     sample_df = pd.read_csv('Sample_Data.csv') #Only has 100 rows
#
#     sample_df.loc[range(10)].to_csv('10_seq.csv', index=False)
#     sample_df.loc[range(50)].to_csv('50_seq.csv', index=False)
#     sample_df.loc[range(100)].to_csv('100_seq.csv', index=False)
#
#     # Increasing the size of the orignal Data set many folds
#     for i in range(5):
#         sample_df = sample_df.append(sample_df)
#
#
#     sample_df.to_csv('500_seq.csv', index=False) #manually cut down ds
#     sample_df.to_csv('1000_seq.csv', index=False) #manually cut down ds



