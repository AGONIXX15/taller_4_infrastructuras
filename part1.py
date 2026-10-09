import random as rd
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

SEED = 42


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

def sec_bloques(blocks: list) -> int:
    return sum(b.sum() for b in blocks)


def generate_matrix(n: int, seed=SEED) -> list[list[int]]:
    rd.seed(seed)
    return [[rd.randint(0, 1000) for _ in range(n)] for _ in range(n)]


def generate_blocks(mat: list[list[int]], bs: int) -> list[Block]:
    n: int = len(mat)
    m: int = len(mat[0])
    return [Block(fi, min(fi + bs, n), ci, min(ci + bs, m))
            for fi in range(0, n, bs) for ci in range(0, m, bs)]


def crear_pool(process: bool, mat, workers: int):
    Executor = ProcessPoolExecutor if process else ThreadPoolExecutor
    return Executor(max_workers=workers, initializer=init_worker, initargs=(mat,))


def run(pool, blocks, workers):
    chunk = max(1, len(blocks) // (workers * 4))
    return sum(pool.map(worker, blocks, chunksize=chunk))


def par(mat: list[list[int]], blocks: list, process: bool, workers: int):
    # el pool se crea aqui, o sea que entra en el tiempo
    with crear_pool(process, mat, workers) as pool:
        return run(pool, blocks, workers)


if __name__ == '__main__':
    m = generate_matrix(200)
    init_worker(m)
    print(sec(m), sec_bloques(generate_blocks(m, 50)), par(m, generate_blocks(m, 50), False, 2))
