#client.py
import calc_amino_acid_composition

import pandas as pd

df = pd.read_csv('Ov_data.csv')

if __name__ == '__main__':
    calc_amino_acid_composition.calculate(Ncores=3, dataframe=df)










#calc_feature.calculate()