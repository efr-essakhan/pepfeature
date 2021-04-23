import pandas as pd
import pepfeature as pep
import timeit

if __name__ == '__main__':

    cores_to_use = 1



    mysetup = '''
import pepfeature as pep
import pandas as pd

rows_10 = pd.read_csv('10_seq.csv')
rows_50 = pd.read_csv('50_seq.csv')
rows_100 = pd.read_csv('100_seq.csv')
rows_500 = pd.read_csv('500_seq.csv')
rows_1000 = pd.read_csv('1000_seq.csv')
    
    '''

    # timeit statements

    #rows_10
    print("10 peptides: "+ str(timeit.timeit(setup=mysetup,stmt=f"pep.aa_all_feat.calc_df(dataframe=rows_10, aa_column='Info_window_seq', Ncores={cores_to_use}, k=2)",
                        number=5)) + " s")

    #rows_50
    print("50 peptides: " + str(timeit.timeit(setup=mysetup,
                                              stmt=f"pep.aa_all_feat.calc_df(dataframe=rows_50, aa_column='Info_window_seq', Ncores={cores_to_use}, k=2)",
                                              number=5)) + " s")

    #rows_100
    print("100 peptides: " + str(timeit.timeit(setup=mysetup,
                                              stmt=f"pep.aa_all_feat.calc_df(dataframe=rows_100, aa_column='Info_window_seq', Ncores={cores_to_use}, k=2)",
                                              number=5)) + " s")

    #rows_500
    print("500 peptides: " + str(timeit.timeit(setup=mysetup,
                                              stmt=f"pep.aa_all_feat.calc_df(dataframe=rows_500, aa_column='Info_window_seq', Ncores={cores_to_use}, k=2)",
                                              number=5)) + " s")

    #rows_1000
    print("1000 peptides: " + str(timeit.timeit(setup=mysetup,
                                               stmt=f"pep.aa_all_feat.calc_df(dataframe=rows_1000, aa_column='Info_window_seq', Ncores={cores_to_use}, k=2)",
                                               number=5)) + " s")






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



