import numpy as np
import time



matrix1 = np.random.randint(0,1000, size=(1000,1000))
matrix2 = np.random.randint(0,1000, size=(1000,1000))


def timeit(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    end = time.perf_counter()
    return (result,end-start)

def smp(mat1: np.matrix, mat2: np.matrix):
    return mat1 @ mat2


def sec(mat1: np.matrix, mat2: np.matrix):
    n = 1_000    

    mat3 = np.zeros((1000,1000))
    for i in range(n):
        for j in range(n):
            acc = 0
            for k in range(n):
                acc +=  mat1[i,k] * mat2[k,j]
            mat3[i,j] = acc
    return mat3

def main():

    result_par, time_par = timeit(smp, matrix1, matrix2)
    result_sec, time_sec = timeit(sec, matrix1, matrix2)

    print(f"paralelo: {time_par : .4f}s")
    print(f"secuencial: {time_sec : .4f}s")
    print(f"mismo resultado: {np.array_equal(result_par,result_sec)}")


if __name__ == '__main__':
    main()
