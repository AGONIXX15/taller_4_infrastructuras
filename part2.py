import numpy as np

SEED = 42


def smp(mat1: np.ndarray, mat2: np.ndarray):
    return mat1 @ mat2


def sec(mat1: list[list[int]], mat2: list[list[int]]):
    n = len(mat1)
    m = len(mat2[0])
    kk = len(mat2)
    mat3 = [[0] * m for _ in range(n)]
    for i in range(n):
        fila = mat1[i]
        for j in range(m):
            acc = 0
            for k in range(kk):
                acc += fila[k] * mat2[k][j]
            mat3[i][j] = acc
    return mat3


def generate_matrices(n: int, seed=SEED):
    rng = np.random.default_rng(seed)
    a = rng.integers(0, 1000, size=(n, n), dtype=np.int64)
    b = rng.integers(0, 1000, size=(n, n), dtype=np.int64)
    return a, b


if __name__ == '__main__':
    a, b = generate_matrices(50)
    print(np.array_equal(np.array(sec(a.tolist(), b.tolist())), smp(a, b)))
