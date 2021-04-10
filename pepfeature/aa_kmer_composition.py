import pandas as pd
from itertools import product
from pepfeature import utils

def _calc_kmer_composition(dataframe: object, k: int, aa_column: str = 'Info_window_seq') -> object:
    """
    Not intended to be called directly by the user, use the functions calculate_csv or calculate_df instead.

    Calculates frequency of each k-length contiguous combination of subsequence of amino acid letters in the
    sequence.

    Since there are 20 valid Amino Acid letters, there can be 400 ( 20x20) possible 2-letter combination,
    8000 (20x20x20) 3-letter combinations, etc.

    Results appended as a new column named feat_freq_{subsequence} e.g. feat_freq_AB, feat_freq_BC etc.

     :param dataframe: A pandas DataFrame
     :param aa_column: Name of column in dataframe consisting of Protein Sequences to process
     :param k: The length of the contiguous combinations of subsequences of the amino acid letters in the sequence
     :return: A Pandas DataFrame containing the calculated features appended as new columns.
     """

    valid_letters = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

    # Create columns for each possible Amino-Acid k-letter combination and fill the values as 0 [e.g. for k=3, with the name format: feat_freq_XXX ]
    dataframe = pd.concat(
        [dataframe, (pd.DataFrame(columns=['feat_freq_{}'.format(''.join(c)) for c in product(''.join(valid_letters), repeat=k)]))])
    dataframe.fillna(0, inplace=True)

    # ==================== Calculate feature ==================== #

    for row in dataframe.itertuples():
        peptide = getattr(row, aa_column)
        kFreq = {}

        # calculate the frequencies of each k-pair of letters in the peptide and store them in kFreq dictionary in the format {Amino-acid-subsequence : Frequency, ...}
        for i in range(len(peptide)):

            k_mer = peptide[i:i + k]

            # Filling dict kFreq
            if len(k_mer) == k:
                if k_mer in kFreq:
                    kFreq[k_mer] += 1
                else:
                    kFreq[k_mer] = 1


        #set the kmer frequencies to corresponding columns for each row of the dataframe
        totalQuantity = sum(kFreq.values())
        for kmer, quantity in kFreq.items():
            dataframe.loc[row.Index, 'feat_freq_{}'.format(kmer)] = (quantity / totalQuantity)

    return dataframe


def calc_csv(k, dataframe, Ncores=4, chunksize = 50000, csv_path_filename = ['', 'result'], aa_column = 'Info_window_seq'): #function that the client should call.
    utils.calculate_export_csv(dataframe = dataframe, function = _calc_kmer_composition, Ncores= Ncores, chunksize= chunksize, csv_path_filename = csv_path_filename, aa_column = aa_column, k=k)

def calc_df(k, dataframe, Ncores=4, chunksize = 50000, aa_column = 'Info_window_seq'): #function that the client should call.
    return utils.calculate_return_df(dataframe = dataframe, function = _calc_kmer_composition, Ncores= Ncores, aa_column = aa_column, chunksize= chunksize, k=k)
