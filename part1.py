import random as rd
import time
import argparse
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor



B = 500
N = 5000

def timeit(fn, *args):

    start =  time.perf_counter()
    ans = fn(*args)
    end = time.perf_counter()
    return (ans, end - start)

class Block:
    __slots__ = ["r_start", "r_end", "c_start", "c_end"]
    def __init__(self, r_start: int, r_end: int, c_start: int, c_end: int) -> None:
        self.r_start = r_start
        self.r_end = r_end
        self.c_start = c_start
        self.c_end = c_end

    def sum(self):
        
        result = 0
        for r in range(self.r_start, self.r_end):
            row = _mat[r]
            for c in range(self.c_start, self.c_end):
                result += row[c]
        return result



def sec(mat: list[list[int]]):
    result: int = 0
    for row in mat:
        for column in row:
            result += column
    return result
            

_mat: list[list[int]] = []
def init_worker(mat: list[list[int]]) -> None:
    global _mat
    _mat = mat

def worker(block: Block):
    return block.sum()

def generate_blocks(mat: list[list[int]], bs=B) -> list[Block]:
    n: int = len(mat)
    m: int = len(mat[0])
    return [Block(fi, min(fi + bs, n), ci, min(ci + bs, m))
            for fi in range(0,n,bs) for ci in range(0,m,bs)]


def par(mat: list[list[int]], b: int, process: bool):
    blocks = generate_blocks(mat)
    Executor = ProcessPoolExecutor if process else ThreadPoolExecutor
    with Executor(initializer=init_worker, initargs=(mat,)) as pool:
        return sum(pool.map(worker,blocks,chunksize=10))


def main():
    matrix: list[list[int]] = [[rd.randint(0,1000) for _ in range(0,N)] for _ in range(0,N)]
    
    result_sec, time_sec = timeit(sec,matrix)
    result_par, time_par = timeit(par,matrix, B, True)
    result_par_th, time_par_th = timeit(par,matrix,B,False)


    print(f"secuencial: {time_sec: .6f}s")
    print(f"paralelo: { time_par : .6f}s")
    print(f"paralelo con threads: {time_par_th : .6f}s")
    print(f"resultado igual?: {result_sec == result_par == result_par_th}")
if __name__ == '__main__':
    main()


