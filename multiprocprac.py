import time
from multiprocessing import Pool #instantiate a pool of workers to be used to distribute our function across the cores/processors on our machine

def sum_square(number):
    s = 0
    for i in range(number):
        s += i*i
    return s


def sum_square_parralel(num):
    start_time = time.perf_counter()
    numbers = range(4)
    p = Pool() #creating a pool obj from the Pool class we just imported
    result = p.map(sum_square, num) #applies the function to the numbers, whilst distributing it on each of the processors
    print(result)
    p.close()
    p.join() # the process will complete and only then any code after can be ran
    end_time = time.perf_counter() - start_time
    print(f'Multi-procceing: processing {len(num)} numbers took {end_time}')

# def sum_square_nmp(num):
#     start_time = time.perf_counter()
#     result = []
#     for i in num:
#         result.append(sum_square(i))
#     end_time = time.perf_counter() -  start_time
#     print(f'No MP: processing {num} numbers took {end_time}')


if __name__ == "__main__":
    #sum_square_nmp(range(100*100))
    sum_square_parralel(list(range(10)))
