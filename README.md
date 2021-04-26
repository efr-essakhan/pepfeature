# Pepfeature
### _A package that consists of functions for calculating epitope/peptide features for prediction purposes_



### What is it

**Pepfeature** is a Python package providing routines for calculating peptide features on a given amino acid sequence.
These features can be used for macine learning purposes such as classification for epitiope prediction.

## Pepfeature Requirements
**Required Software/Tools:**  
- Tested on Python 3.8 (other Python 3 versions probably work too)

**Required Package Dependencies:**  
(Pepfeature has been tested on these versions of the dependancies. More recent versions of these dependancies may also be compatible with the Package.)
- et-xmlfile v1.1.0
- setuptools v56.0.0
- numpy v1.20.2
- openpyxl v3.0.7
- pandas v1.2.4
- python-dateutil v2.8.1
- pytz v2021.1
- six v1.15.0


## Installation

```
pip install Pepfeature
```
(All dependancies are expected to be automatically installed asswell with this 'pip install pepfeature' command.)
The source code is currently hosted on GitHub at: https://github.com/essakh/pepfeature

## Example Use
**NOTE: The Github contains an 'examples.py' in the root folder with many example use cases**

**Ensure at all times that any lines of code that utilize this package are executed within the code block:**
```python
if __name__ == '__main__':
```
Example:
```python
import pepfeature as pep
import pandas

df = pd.read_csv('pepfeature/data/Sample_Data.csv')

#Use of pepfeature
if __name__ == '__main__':
    #Calculate all features on df
    df_feat = pep.aa_all_feat.calc_df(dataframe=df, aa_column='Info_window_seq', Ncores=4, k=2)
 
    print(df_feat) #print the data frame to console
```


## API

The API follows this structure:
![line of code](./pictures/generic_string.png)

Please see pepfeature/examples.py for example use cases.

Also see the attached API of each function/ algorithm, for a complete documentation.


## Contributing to pepfeature

All contributions, bug reports, bug fixes, documentation improvements, enhancements and ideas are welcome.
