# Pepfeature
### _A package that consists of functions for calculating epitope/peptide features for prediction purposes_



### What is it

**Pepfeature** is a Python package providing routines for calculating peptide features on a given amino acid sequence.
These features can be used for macine learning purposes such as classification for epitiope prediction.

## Pepfeature Requirements
**Required Software/Tools:**  
- Python 3.8

**Required Package Dependencies:**  
- panadas
- numpy
- setuptools
- openpyxl

## Installation

```
pip install Pepfeature
```
(All missing dependancies are expected to be installed asswell with this 'pip install'.)
The source code is currently hosted on GitHub at: https://github.com/essakh/pepfeature

## Example Use
**NOTE: The Github contains an 'examples.py' with many example use cases**

Example:
```python
import pepfeature as pep
import pandas

df = pd.read_csv('pepfeature/data/Sample_Data.csv')

#Use of pepfeature
if __name__ == '__main__':
    df_feat = pep.aa_all_feat.calc_df(dataframe=df, aa_column='Info_window_seq', Ncores=4, k=2)
 
    print(df_feat)
```


## How to use it

**Ensure at all times that any lines of code that utilize this package are encapsulated within the code block.**
```python
if __name__ == '__main__':
```

Please see pepfeature/examples.py for example use cases.

Also see the attached API of each function/ algorithm, for a complete documentation.


## Contributing to pepfeature

All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.
