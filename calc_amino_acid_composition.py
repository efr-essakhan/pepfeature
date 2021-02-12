#calc_amino_acid_composition.py

from multiprocessing import Pool
import numpy as np
import pandas

def calc_aa_composition(dataframe):

    # Dictionary mapping each Amino-Acid to its respective group-value
    AA_groups_dict = {'Tiny': ["A", "C", "G", "S", "T"], 'Small': ["A", "B", "C", "D", "G", "N", "P", "S", "T", "V"],
                       'Aliphatic': ["A", "I", "L", "V"], 'Aromatic': ["F", "H", "W", "Y"],'NonPolar':["A", "C", "F", "G", "I", "L", "M", "P", "V", "W", "Y"],
                       'Polar':["D", "E", "H", "K", "N", "Q", "R", "S", "T", "Z"],'Charged':["B", "D", "E", "H", "K", "R", "Z"],'Basic':["H", "K", "R"],
                       'Acidic':["B", "D", "E", "Z"]}

    # ==================== Calculate feature ==================== #

    for row in dataframe.itertuples():

        peptide = row.Info_window_seq
        peptide_length = len(peptide)

        for group_name, group_aa_values in AA_groups_dict.items():
            count = 0
            for aa in peptide:
                #accumlate number of times the aas appears in the particular group
                count += group_aa_values.count(aa)

            # set the frequency to corresponding columns for each row of the dataframe, column is automatically created if it doesn't exist
            dataframe.loc[row.Index, 'feat_Perc_{}'.format(group_name)] = (count / peptide_length) * 100

    return dataframe

def calculate(Ncores, dataframe): #function that the client should call.

    # # Firstly Split the dataframe into 4 chunks
    # list_df = chunks(dataframe, 4) #arbitrary
    data = np.split(dataframe, range(12, len(dataframe), 12))

    # creating a pool obj
    p = Pool(processes=Ncores)

    # apply the function to the dfd, whilst distributing it on each of the processors
    result_df = p.map(calc_aa_composition, dataframe)

    p.close()
    p.join() # the process will complete and only then any code after can be ran

    print(result_df)
    #return result_df