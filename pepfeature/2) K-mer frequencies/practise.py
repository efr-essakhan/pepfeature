import pandas as pd
import concurrent.futures
import dask.dataframe as dd
import time

start = time.perf_counter()




def do_something(seconds):
    print(f'Sleeping for {seconds} second(s)')
    time.sleep(seconds)
    return 'Done sleeping...'



if __name__ == '__main__':


    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(do_something, 1) for _ in range(10)]

        for f in concurrent.futures.as_completed(results):
            print(f.result())



    # processes = []
    # for _ in range(10):
    #     p = multiprocessing.Process(target=do_something, args=[1.5])
    #     p.start()
    #     processes.append(p)
    #
    # for process in processes:
    #     process.join()

    finish = time.perf_counter()
    print(f'Finished in {round(finish-start,4)} seconds')