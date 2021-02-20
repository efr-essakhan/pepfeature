import multiprocessing as mp
import pandas as pd
import numpy as np
import time
import os
import sys

pd.set_option("display.max_columns", None)

df = pd.read_csv('Ov_data.csv')

def just_wait_and_print_len_and_idx(df):
    """Waits for 5 seconds and prints df length and first and last index"""
    # Extract some info
    idx_values = df.index.values
    first_idx, last_idx = idx_values[0], idx_values[-1]
    length = len(df)
    pid = os.getpid()

    # Waste some CPU cycles
    time.sleep(1)

    # Print the info
    print('First idx {}, last idx {} and len {} '
          'from process {}'.format(first_idx, last_idx, length, pid))


def df_chunking(df, chunksize):
    """Splits df into chunks, drops data of original df inplace"""
    count = 0 # Counter for chunks
    while len(df):
        count += 1
        print(f'Preparing chunk {count}')
        # Return df chunk
        yield df.iloc[:chunksize].copy()
        # Delete data in place because it is no longer needed
        df.drop(df.index[:chunksize], inplace=True)


def main():
    # Job parameters
    n_jobs = 4  # Poolsize
    size = (10000, 1000)  # Size of DataFrame
    chunksize = 100  # Maximum size of Frame Chunk

    # Preparation
    df = pd.DataFrame(np.random.rand(*size))

    pool = mp.Pool(n_jobs)

    print('Starting MP')

    # Execute the wait and print function in parallel
    pool.imap(just_wait_and_print_len_and_idx, df_chunking(df, chunksize))

    pool.close()
    pool.join()

    print('DONE')



def append_lst():
    lst = []
    for i in range(1000):
        lst.append(i)


if __name__ == '__main__':
    #main()

    #append_lst()
    df_chunking(df.loc[1], 1)
    yolo = df_chunking(df.loc[1], 1)
    print(yolo)




    #print(just_wait_and_print_len_and_idx(df))

