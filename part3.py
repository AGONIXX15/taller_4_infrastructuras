from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import numpy as np

SEED = 42


class Block:
    __slots__ = ["r_start", "r_end", "c_start", "c_end"]
    def __init__(self, r_start: int, r_end: int, c_start: int, c_end: int) -> None:
        self.r_start = r_start
        self.r_end = r_end
        self.c_start = c_start
        self.c_end = c_end

    def sum(self):
        # int64 para que no desborde el int32
        blk = _mat[self.r_start:self.r_end, self.c_start:self.c_end]
        return int(blk.sum(axis=1, dtype=np.int64).sum())


def sec(mat: np.ndarray):
    result: int = 0
    for row in mat:
        for column in row.tolist():
            result += column
    return result


_mat: np.ndarray = None
def init_worker(mat: np.ndarray) -> None:
    global _mat
    _mat = mat

def worker(block: Block):
    return block.sum()

def worker_slice(trozo: np.ndarray):
    return int(trozo.sum(axis=1, dtype=np.int64).sum())

def sec_blocks(blocks):
    return sum(b.sum() for b in blocks)


def generate_matrix(n: int, seed=SEED) -> np.ndarray:
    return np.random.default_rng(seed).integers(0, 1001, size=(n, n), dtype=np.int32)


def generate_blocks(mat: np.ndarray, bs: int) -> list[Block]:
    n, m = mat.shape
    return [Block(fi, min(fi + bs, n), ci, min(ci + bs, m))
            for fi in range(0, n, bs) for ci in range(0, m, bs)]


def crear_pool(process: bool, mat: np.ndarray, workers: int):
    if process:
        return ProcessPoolExecutor(max_workers=workers)
    return ThreadPoolExecutor(max_workers=workers, initializer=init_worker, initargs=(mat,))


def run(pool, blocks, workers):
    chunk = max(1, len(blocks) // (workers * 4))
    return sum(pool.map(worker, blocks, chunksize=chunk))

def run_procesos(pool, mat, blocks):
    # cada bloque se copia contiguo y viaja como argumento (no mandamos la matriz entera)
    trozos = [np.ascontiguousarray(mat[b.r_start:b.r_end, b.c_start:b.c_end]) for b in blocks]
    return sum(pool.map(worker_slice, trozos))


if __name__ == '__main__':
    m = generate_matrix(1000)
    init_worker(m)
    print(int(m.sum(dtype=np.int64)), sec_blocks(generate_blocks(m, 250)))
