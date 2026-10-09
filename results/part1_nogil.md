# Parte 1: SMP (Python puro)

## Sistema

- Python: 3.14.7
- Build free-threaded (Py_GIL_DISABLED): True
- GIL habilitado: False
- CPUs logicas: 12
- NumPy: 2.5.3
- Plataforma: Linux-7.2.4-arch1-2-x86_64-with-glibc2.44
- Fecha: 2026-10-08T17:47:05

## N=1000, bloque=100

| n bloques | config | p | t (s) | min | mediana | CV% | speedup | efic. |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | secuencial por bloques (base) | 1 | 0.02129 ± 0.00022 | 0.021 | 0.02129 | 1.011 | 1 ± 0 | 1 |
| 100 | referencia: bucle plano sin bloques | 1 | 0.017 ± 0.00033 | 0.01673 | 0.01686 | 1.95 | 1.252 ± 0.028 | 1.252 |
| 100 | threads+pool | 1 | 0.03067 ± 0.0021 | 0.02812 | 0.03002 | 6.834 | 0.6942 ± 0.048 | 0.6942 |
| 100 | threads (pool reutilizado) | 1 | 0.02795 ± 0.00049 | 0.02703 | 0.028 | 1.77 | 0.7616 ± 0.016 | 0.7616 |
| 100 | threads+pool | 2 | 0.01721 ± 0.00064 | 0.01629 | 0.01722 | 3.737 | 1.237 ± 0.048 | 0.6185 |
| 100 | threads (pool reutilizado) | 2 | 0.01588 ± 0.0007 | 0.01527 | 0.01565 | 4.435 | 1.341 ± 0.061 | 0.6705 |
| 100 | threads+pool | 4 | 0.009989 ± 0.00057 | 0.00899 | 0.009936 | 5.703 | 2.131 ± 0.12 | 0.5328 |
| 100 | threads (pool reutilizado) | 4 | 0.008995 ± 0.00058 | 0.008177 | 0.008885 | 6.447 | 2.367 ± 0.15 | 0.5917 |
| 100 | threads+pool | 8 | 0.007506 ± 0.0011 | 0.006574 | 0.006985 | 14.9 | 2.836 ± 0.42 | 0.3545 |
| 100 | threads (pool reutilizado) | 8 | 0.006032 ± 0.00012 | 0.005831 | 0.006041 | 2.033 | 3.529 ± 0.08 | 0.4412 |
| 100 | threads+pool | 12 | 0.007088 ± 0.00037 | 0.006463 | 0.007118 | 5.185 | 3.003 ± 0.16 | 0.2503 |
| 100 | threads (pool reutilizado) | 12 | 0.005212 ± 0.0002 | 0.004906 | 0.005207 | 3.795 | 4.085 ± 0.16 | 0.3404 |
| 100 | procesos+pool | 1 | 0.07176 ± 0.0015 | 0.07001 | 0.07115 | 2.059 | 0.2967 ± 0.0068 | 0.2967 |
| 100 | procesos (pool reutilizado) | 1 | 0.02435 ± 0.0024 | 0.02178 | 0.02311 | 9.68 | 0.8742 ± 0.085 | 0.8742 |
| 100 | procesos+pool | 2 | 0.1034 ± 0.0026 | 0.1004 | 0.1029 | 2.545 | 0.206 ± 0.0056 | 0.103 |
| 100 | procesos (pool reutilizado) | 2 | 0.014 ± 0.00081 | 0.01253 | 0.01378 | 5.801 | 1.52 ± 0.09 | 0.7601 |
| 100 | procesos+pool | 4 | 0.1831 ± 0.0027 | 0.1791 | 0.1824 | 1.489 | 0.1163 ± 0.0021 | 0.02907 |
| 100 | procesos (pool reutilizado) | 4 | 0.008319 ± 0.00054 | 0.007458 | 0.008237 | 6.501 | 2.559 ± 0.17 | 0.6398 |
| 100 | procesos+pool | 8 | 0.311 ± 0.0036 | 0.3049 | 0.3111 | 1.158 | 0.06845 ± 0.0011 | 0.008556 |
| 100 | procesos (pool reutilizado) | 8 | 0.006582 ± 0.00081 | 0.005611 | 0.006178 | 12.36 | 3.235 ± 0.4 | 0.4043 |
| 100 | procesos+pool | 12 | 0.4057 ± 0.006 | 0.3959 | 0.4075 | 1.487 | 0.05248 ± 0.00094 | 0.004373 |
| 100 | procesos (pool reutilizado) | 12 | 0.01272 ± 0.014 | 0.006346 | 0.008154 | 113.2 | 1.674 ± 1.9 | 0.1395 |

## N=1000, bloque=50

| n bloques | config | p | t (s) | min | mediana | CV% | speedup | efic. |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 400 | secuencial por bloques (base) | 1 | 0.02302 ± 0.0017 | 0.02203 | 0.02226 | 7.28 | 1 ± 0 | 1 |
| 400 | procesos (pool reutilizado) | 12 | 0.01201 ± 0.012 | 0.006425 | 0.007935 | 103.5 | 1.917 ± 2 | 0.1598 |

## N=1000, bloque=200

| n bloques | config | p | t (s) | min | mediana | CV% | speedup | efic. |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 25 | secuencial por bloques (base) | 1 | 0.02052 ± 0.00012 | 0.02023 | 0.02054 | 0.5883 | 1 ± 0 | 1 |
| 25 | procesos (pool reutilizado) | 12 | 0.01968 ± 0.029 | 0.005422 | 0.0071 | 148.8 | 1.043 ± 1.6 | 0.08689 |

## N=1000, bloque=500

| n bloques | config | p | t (s) | min | mediana | CV% | speedup | efic. |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | secuencial por bloques (base) | 1 | 0.02071 ± 0.00059 | 0.02023 | 0.02054 | 2.837 | 1 ± 0 | 1 |
| 4 | procesos (pool reutilizado) | 12 | 0.008082 ± 0.0009 | 0.006996 | 0.007997 | 11.08 | 2.563 ± 0.29 | 0.2136 |

## Notas

- Los '±' son la desviacion estandar muestral (ddof=1) de las corridas individuales; '-' si hubo una sola corrida.
- Semilla=42, reps=[10] (+1 warmup descartado).
- '+pool' incluye la creacion del pool en cada medicion (con procesos, el arranque de los workers; con forkserver cada worker reimporta el modulo, numpy incluido); '(pool reutilizado)' no.
- Los bloques se generan fuera de la region cronometrada. En el barrido de bloque, con bloque=500 solo hay 4 bloques para 12 workers, lo que limita el paralelismo.
- Speedup respecto a la suma secuencial sobre los mismos bloques (sec_bloques); el bucle plano es solo referencia.
- Todos los resultados se verifican contra la suma secuencial (RuntimeError si difieren).
