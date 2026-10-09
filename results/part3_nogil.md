# Parte 3: SMP + SIMD

## Sistema

- Python: 3.14.7
- Build free-threaded (Py_GIL_DISABLED): True
- GIL habilitado: False
- CPUs logicas: 12
- NumPy: 2.5.3
- Plataforma: Linux-7.2.4-arch1-2-x86_64-with-glibc2.44
- Fecha: 2026-10-08T17:52:34

## N=10000, bloque=1000

| config | p | t (s) | min | mediana | CV% | speedup | efic. | GB/s |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| secuencial NumPy (bloques) | 1 | 0.04676 ± 0.0025 | 0.04493 | 0.04582 | 5.274 | 1 ± 0 | 1 | 8.555 |
| mat.sum() directo | 1 | 0.03632 ± 0.0015 | 0.03538 | 0.03581 | 4.005 | 1.287 ± 0.085 | 1.287 | 11.01 |
| Python puro (ESTIMADO) | 1 | 2.766 ± 0.03 | 2.749 | 2.75 | 1.068 | - | - | - |
| threads | 1 | 0.04859 ± 0.00096 | 0.0472 | 0.04848 | 1.984 | 0.9622 ± 0.054 | 0.9622 | 8.232 |
| threads | 2 | 0.02729 ± 0.00069 | 0.02649 | 0.02716 | 2.51 | 1.713 ± 0.1 | 0.8567 | 14.66 |
| threads | 4 | 0.01719 ± 0.00028 | 0.01677 | 0.01725 | 1.652 | 2.72 ± 0.15 | 0.68 | 23.27 |
| threads | 8 | 0.0144 ± 0.00013 | 0.01423 | 0.01438 | 0.9185 | 3.247 ± 0.17 | 0.4059 | 27.78 |
| threads | 12 | 0.01464 ± 0.00043 | 0.01392 | 0.01482 | 2.925 | 3.194 ± 0.19 | 0.2661 | 27.32 |
| procesos (bloque como argumento) | 1 | 0.603 ± 0.005 | 0.5932 | 0.6027 | 0.8352 | 0.07754 ± 0.0041 | 0.07754 | 0.6633 |
| procesos (bloque como argumento) | 2 | 0.6344 ± 0.0078 | 0.6244 | 0.6328 | 1.237 | 0.0737 ± 0.004 | 0.03685 | 0.6305 |
| procesos (bloque como argumento) | 4 | 0.8111 ± 0.01 | 0.7966 | 0.8089 | 1.24 | 0.05764 ± 0.0031 | 0.01441 | 0.4931 |
| procesos (bloque como argumento) | 8 | 0.884 ± 0.041 | 0.8406 | 0.8746 | 4.592 | 0.05289 ± 0.0037 | 0.006611 | 0.4525 |
| procesos (bloque como argumento) | 12 | 0.886 ± 0.014 | 0.8623 | 0.8908 | 1.622 | 0.05277 ± 0.0029 | 0.004398 | 0.4515 |

## Notas

- Los '±' son la desviacion estandar muestral (ddof=1) de las corridas individuales; '-' si hubo una sola corrida.
- int32, semilla=42, reps=[3, 10] (+1 warmup descartado).
- Pools creados una vez por configuracion fuera de la region cronometrada; el arranque de los workers queda fuera del tiempo.
- Procesos: cada bloque se copia y se envia como argumento (pickle); copia y serializacion estan incluidas en el tiempo. Solo concurrent.futures.
- GB/s = bytes de la matriz / tiempo (ancho de banda efectivo de lectura).
- Python puro: ESTIMADO por extrapolacion de un bloque; no medido, sin speedup.
