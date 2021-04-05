#' Calculate statistical and physicochemical features for peptides
#'
#' This function is used to calculate several distinct families of features for
#' a vector of peptides.

from pepfeature import calc_aa_composition
from pepfeature import calc_aa_descriptors
from pepfeature import calc_aa_percentages
from pepfeature import calc_cojoint_triads
from pepfeature import calc_molecular_weight
from pepfeature import calc_number_of_atoms
from pepfeature import calc_sequence_entropy

module_names = [
    calc_aa_composition,
    calc_aa_descriptors,
    calc_aa_percentages,
    calc_cojoint_triads,
    calc_molecular_weight,
    calc_number_of_atoms,
    calc_sequence_entropy
]

def calc_all_features_csv(dataframe, csv_path_filename, Ncores=4, chunksize=50000):

    for module in module_names:
        module.calculate_csv(dataframe=dataframe, Ncores=Ncores,
                                   chunksize=chunksize, csv_path_filename=csv_path_filename)


def calc_all_features_df(dataframe, Ncores=4, chunksize=50000):
    
    for module in module_names:
        module.calculate_df(dataframe=dataframe, Ncores=Ncores,
                             chunksize=chunksize)
