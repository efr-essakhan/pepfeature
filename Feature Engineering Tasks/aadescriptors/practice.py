import pandas as pd
import numpy as np
import time
from aadescriptors import aadesc

pd.set_option("display.max_columns", None)

dc = pd.read_csv('Ov_data.csv')

start_time = time.time()
print(aadesc.aadesc(dc))
print("--- %s seconds ---" % (time.time() - start_time))