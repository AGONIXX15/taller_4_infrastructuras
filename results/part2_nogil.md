# Parte 2: SIMD (NumPy vs bucle triple)

## Sistema

- Python: 3.14.7
- Build free-threaded (Py_GIL_DISABLED): True
- GIL habilitado: False
- CPUs logicas: 12
- NumPy: 2.5.3
- Plataforma: Linux-7.2.4-arch1-2-x86_64-with-glibc2.44
- Fecha: 2026-10-08T17:51:47
- Modo BLAS: 1hilo
- env OPENBLAS_NUM_THREADS: 1
- env OMP_NUM_THREADS: 1
- env MKL_NUM_THREADS: 1

## Multiplicacion de matrices

| N | t Python (s) | t NumPy int64 (s) | t NumPy f64 (s) | speedup int64 | speedup f64 | f64 vs int64 | GFLOP/s py | GFLOP/s int64 | GFLOP/s f64 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 0.04102 ± 0.00048 | 0.0004197 ± 1.8e-05 | 8.242e-05 ± 9.9e-06 | 97.74 | 497.7 | 5.092 | 0.04876 | 4.766 | 24.27 |
| 200 | 0.3492 ± 0.0044 | 0.002924 ± 9.1e-05 | 0.0003734 ± 3e-05 | 119.4 | 935.4 | 7.833 | 0.04581 | 5.471 | 42.85 |
| 300 | 1.21 ± 0.0062 | 0.0118 ± 0.00051 | 0.001038 ± 5.3e-05 | 102.6 | 1167 | 11.37 | 0.04461 | 4.577 | 52.04 |
| 500 | 7.945 ± 0.045 | 0.05927 ± 0.0014 | 0.004631 ± 0.00014 | 134 | 1716 | 12.8 | 0.03146 | 4.218 | 53.98 |
| 1000 | 71.63 ± 1.1 | 0.6331 ± 0.026 | 0.03249 ± 0.001 | 113.1 | 2205 | 19.49 | 0.02792 | 3.159 | 61.56 |

## Notas

- Los '±' son la desviacion estandar muestral (ddof=1) de las corridas individuales; '-' si hubo una sola corrida.
- Semilla=42; reps Python puro por N: [5, 5, 5, 5, 3]; reps NumPy: [20].
- Exponente log-log de t vs N (ajuste con N=[300, 500, 1000]): Python puro 3.38, NumPy int64 3.31, NumPy float64 2.86 (teorico 3).
- Con N chico el exponente de NumPy lo domina el overhead y el cache, no es comparable con el 3 teorico.
- Los casos de Python puro con n>=500 tienen warmup=0.
- Bucle tradicional i-j-k sobre listas de Python (.tolist()); resultado verificado contra NumPy.
- Modo BLAS: 1 hilo (OPENBLAS/OMP/MKL_NUM_THREADS=1): float64 aisla SIMD.
- float64 usa BLAS (SIMD); int64 no usa BLAS, usa un bucle interno de NumPy.
