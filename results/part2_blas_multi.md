# Parte 2: SIMD (NumPy vs bucle triple)

## Sistema

- Python: 3.14.7
- Build free-threaded (Py_GIL_DISABLED): False
- GIL habilitado: True
- CPUs logicas: 12
- NumPy: 2.5.3
- Plataforma: Linux-7.2.4-arch1-2-x86_64-with-glibc2.44
- Fecha: 2026-10-08T17:57:36
- Modo BLAS: multi
- env OPENBLAS_NUM_THREADS: (sin definir)
- env OMP_NUM_THREADS: (sin definir)
- env MKL_NUM_THREADS: (sin definir)

## Multiplicacion de matrices

| N | t Python (s) | t NumPy int64 (s) | t NumPy f64 (s) | speedup int64 | speedup f64 | f64 vs int64 | GFLOP/s py | GFLOP/s int64 | GFLOP/s f64 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 0.04354 ± 0.00074 | 0.0004274 ± 1.6e-05 | 6.065e-05 ± 8.9e-06 | 101.9 | 717.9 | 7.047 | 0.04593 | 4.679 | 32.98 |
| 200 | 0.372 ± 0.011 | 0.003023 ± 0.00013 | 0.0002308 ± 0.00024 | 123 | 1612 | 13.1 | 0.04301 | 5.292 | 69.32 |
| 300 | 1.3 ± 0.0089 | 0.01145 ± 0.00019 | 0.0003407 ± 7.1e-05 | 113.5 | 3816 | 33.62 | 0.04152 | 4.714 | 158.5 |
| 500 | 7.678 ± 0.16 | 0.05737 ± 0.0014 | 0.001289 ± 0.00013 | 133.8 | 5957 | 44.51 | 0.03256 | 4.358 | 194 |
| 1000 | 69.54 ± 0.41 | 0.7333 ± 0.026 | 0.01059 ± 0.0013 | 94.84 | 6567 | 69.24 | 0.02876 | 2.728 | 188.9 |

## Notas

- Los '±' son la desviacion estandar muestral (ddof=1) de las corridas individuales; '-' si hubo una sola corrida.
- Semilla=42; reps Python puro por N: [5, 5, 5, 5, 3]; reps NumPy: [20].
- Exponente log-log de t vs N (ajuste con N=[300, 500, 1000]): Python puro 3.30, NumPy int64 3.47, NumPy float64 2.86 (teorico 3).
- Con N chico el exponente de NumPy lo domina el overhead y el cache, no es comparable con el 3 teorico.
- Los casos de Python puro con n>=500 tienen warmup=0.
- Bucle tradicional i-j-k sobre listas de Python (.tolist()); resultado verificado contra NumPy.
- Modo BLAS: MULTIHILO (float64 mezcla SMP con SIMD).
- float64 usa BLAS (SIMD); int64 no usa BLAS, usa un bucle interno de NumPy.
