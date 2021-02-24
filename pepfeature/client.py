#from pepfeature import calc_kmer_composition as aa
from pepfeature import calc_aa_composition
from pepfeature import calc_aa_descriptors
from pepfeature import calc_aa_percentages
from pepfeature import calc_cojoint_triads
from pepfeature import calc_molecular_weight
from pepfeature import calc_number_of_atoms
from pepfeature import calc_sequence_entropy
import pandas as pd
import time


from pepfeature import *

# df = pd.read_csv('Ov_data.csv')
df = pd.DataFrame(data={'Info_window_seq' : ['CCAKJATJXARRRZS', 'LLLLLLLLDVHIESG']})
if __name__ == '__main__':
    start = time.time()


    #print(aa.calculate_csv(k=2, Ncores=1, dataframe = df.loc[range(1)], chunksize = 5))
    #print(aa.calculate_csv(Ncores=1, dataframe=df.loc[range(1)], chunksize=5))
    #print(calc_aa_descriptors.calculate_csv(Ncores=1, dataframe=df.loc[range(1)], chunksize=1, csv_path_filename=[r'C:\Users\Essa Khan\Desktop\dataframes', 'yolo']))
    #print(calc_aa_percentages.calculate_csv(Ncores=1, dataframe=df.loc[range(1)], chunksize=1, csv_path_filename=[r'C:\Users\Essa Khan\Desktop\dataframes', 'yolo']))
    #print(calc_cojoint_triads.calculate_csv(Ncores=1, dataframe=df.loc[range(1)], chunksize=1, csv_path_filename=[r'C:\Users\Essa Khan\Desktop\dataframes', 'yolo']))
    #print(calc_molecular_weight.calculate_csv(Ncores=1, dataframe=df.loc[range(1)], chunksize=1, csv_path_filename=[r'C:\Users\Essa Khan\Desktop\dataframes', 'yolo']))
    #print(calc_number_of_atoms.calculate_csv(Ncores=1, dataframe=df.loc[range(1)], chunksize=1, csv_path_filename=[r'C:\Users\Essa Khan\Desktop\dataframes', 'yolo']))
    #print(calc_sequence_entropy.calculate_csv(Ncores=1, dataframe=df.loc[range(1)], chunksize=1, csv_path_filename=[r'C:\Users\Essa Khan\Desktop\dataframes', 'yolo']))
    print(calc_sequence_entropy.calculate_csv(Ncores=1, dataframe=df, chunksize=1, csv_path_filename=[r'C:\Users\Essa Khan\Desktop\dataframes', 'yolo']))

    #help(pepfeature)
    #, chunksize=1, csv_path_filename=[r'C:\Users\Essa Khan\Desktop\dataframes', 'test'] ,
    # for gm_chunk in pd.read_csv('Ov_data.csv', chunksize=20000):
    #     print(calc_amino_acid_composition.calculate(dataframe=gm_chunk,
    #                                                 Ncores=multiprocessing.cpu_count(), chunksize=0,
    #                                                 csv_path=r'C:\Users\Essa Khan\Desktop\Pepfeature dataframes'))
    #Above works and took 118.22979235649109 s ['Ov_data.csv' chunksize=10000 , chunksize=10000]

    # df.loc[range(50000)]
    # calc_amino_acid_composition.dummydataframe()
    # print(calc_amino_acid_composition.calc_aa_composition(df.loc[range(50000)]))
    # dataframe=df.loc[range(10)]
    # print(calc_amino_acid_composition.calculate(df.loc[range(10)], chunksize = 2))
    print(f'time taken: {time.time() - start}')

    # 9.474778175354004 4,2000
    # 19.15898585319519,4,2000
    # Without using NCORE:  19.768373250961304

    # -----
    # 54.72946786880493, 50k, 4, 10k
    # 31.59996223449707, 50k, multiprocessing.cpu_count(), 10k
    # 141.61061215400696 50k no cores

# for x, y in [[1, 2], ['a', 'b']]:
#     print(f'{x} and {y}')
#     #print(y)


# print(df.Info_n_Negative)

# start = time.time()
# calc_amino_acid_composition.calc_aa_composition(df)
# print(f'time taken: {time.time()-start}')


# 1 core: time taken: 223.05973744392395
# max cores: 92.77946376800537
# without core: and chunking: 466.0802357196808


# calc_feature.calculate()
