# Parte 2: SIMD (NumPy vs bucle triple)

## Sistema

- Python: 3.14.7
- Build free-threaded (Py_GIL_DISABLED): False
- GIL habilitado: True
- CPUs logicas: 12
- NumPy: 2.5.3
- Plataforma: Linux-7.2.4-arch1-2-x86_64-with-glibc2.44
- Fecha: 2026-10-08T17:46:15
- Modo BLAS: 1hilo
- env OPENBLAS_NUM_THREADS: 1
- env OMP_NUM_THREADS: 1
- env MKL_NUM_THREADS: 1

## Multiplicacion de matrices

| N | t Python (s) | t NumPy int64 (s) | t NumPy f64 (s) | speedup int64 | speedup f64 | f64 vs int64 | GFLOP/s py | GFLOP/s int64 | GFLOP/s f64 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 0.04375 ± 0.001 | 0.000467 ± 7.7e-05 | 9.932e-05 ± 3.2e-05 | 93.67 | 440.5 | 4.702 | 0.04572 | 4.283 | 20.14 |
| 200 | 0.4058 ± 0.035 | 0.0035 ± 0.0012 | 0.000389 ± 2.7e-05 | 116 | 1043 | 8.997 | 0.03943 | 4.572 | 41.13 |
| 300 | 1.423 ± 0.096 | 0.01222 ± 0.00055 | 0.00119 ± 0.00036 | 116.4 | 1196 | 10.27 | 0.03796 | 4.42 | 45.39 |
| 500 | 8.024 ± 0.23 | 0.06158 ± 0.0041 | 0.004418 ± 0.00015 | 130.3 | 1816 | 13.94 | 0.03116 | 4.06 | 56.59 |
| 1000 | 69.64 ± 0.17 | 0.6178 ± 0.01 | 0.03755 ± 0.00062 | 112.7 | 1855 | 16.45 | 0.02872 | 3.237 | 53.27 |

## Notas

- Los '±' son la desviacion estandar muestral (ddof=1) de las corridas individuales; '-' si hubo una sola corrida.
- Semilla=42; reps Python puro por N: [5, 5, 5, 5, 3]; reps NumPy: [20].
- Exponente log-log de t vs N (ajuste con N=[300, 500, 1000]): Python puro 3.23, NumPy int64 3.26, NumPy float64 2.88 (teorico 3).
- Con N chico el exponente de NumPy lo domina el overhead y el cache, no es comparable con el 3 teorico.
- Los casos de Python puro con n>=500 tienen warmup=0.
- Bucle tradicional i-j-k sobre listas de Python (.tolist()); resultado verificado contra NumPy.
- Modo BLAS: 1 hilo (OPENBLAS/OMP/MKL_NUM_THREADS=1): float64 aisla SIMD.
- float64 usa BLAS (SIMD); int64 no usa BLAS, usa un bucle interno de NumPy.
