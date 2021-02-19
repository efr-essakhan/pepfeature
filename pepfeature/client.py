#client.py
from pepfeature import calc_amino_acid_composition
#import pepfeature

import pandas as pd
import time
import multiprocessing
import os
import psutil

df = pd.read_csv('Ov_data.csv')

if __name__ == '__main__':
    start = time.time()

    process = psutil.Process(os.getpid())
    print(f'before memory usage {process.memory_percent()}')
    print(calc_amino_acid_composition.calculate(dataframe=calc_amino_acid_composition.dummydataframe(100000), Ncores=multiprocessing.cpu_count(), chunksize=50000, csv_path='300k'))
    print(f'after memory usage {process.memory_percent()}')
    #df.loc[range(50000)]
    #calc_amino_acid_composition.dummydataframe()
    #print(calc_amino_acid_composition.calc_aa_composition(df.loc[range(50000)]))
    #dataframe=df.loc[range(10)]
    #print(calc_amino_acid_composition.calculate(df.loc[range(10)], chunksize = 2))
    print(f'time taken: {time.time()-start}')

    #9.474778175354004 4,2000
    #19.15898585319519,4,2000
    #Without using NCORE:  19.768373250961304

    #-----
    #54.72946786880493, 50k, 4, 10k
    #31.59996223449707, 50k, multiprocessing.cpu_count(), 10k
    #141.61061215400696 50k no cores




# for x, y in [[1, 2], ['a', 'b']]:
#     print(f'{x} and {y}')
#     #print(y)


#print(df.Info_n_Negative)

# start = time.time()
# calc_amino_acid_composition.calc_aa_composition(df)
# print(f'time taken: {time.time()-start}')


#1 core: time taken: 223.05973744392395
#max cores: 92.77946376800537
#without core: and chunking: 466.0802357196808




#calc_feature.calculate()