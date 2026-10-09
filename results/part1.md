# Parte 1: SMP (Python puro)

## Sistema

- Python: 3.14.7
- Build free-threaded (Py_GIL_DISABLED): False
- GIL habilitado: True
- CPUs logicas: 12
- NumPy: 2.5.3
- Plataforma: Linux-7.2.4-arch1-2-x86_64-with-glibc2.44
- Fecha: 2026-10-08T17:52:58

## N=1000, bloque=100

| n bloques | config | p | t (s) | min | mediana | CV% | speedup | efic. |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | secuencial por bloques (base) | 1 | 0.02706 ± 0.0013 | 0.02631 | 0.02649 | 4.926 | 1 ± 0 | 1 |
| 100 | referencia: bucle plano sin bloques | 1 | 0.0183 ± 0.00019 | 0.01805 | 0.01828 | 1.052 | 1.479 ± 0.074 | 1.479 |
| 100 | threads+pool | 1 | 0.03141 ± 0.002 | 0.02844 | 0.03187 | 6.324 | 0.8613 ± 0.069 | 0.8613 |
| 100 | threads (pool reutilizado) | 1 | 0.02903 ± 0.00013 | 0.02885 | 0.02899 | 0.4494 | 0.9321 ± 0.046 | 0.9321 |
| 100 | threads+pool | 2 | 0.03346 ± 0.0039 | 0.0304 | 0.03266 | 11.62 | 0.8085 ± 0.1 | 0.4043 |
| 100 | threads (pool reutilizado) | 2 | 0.02841 ± 0.0007 | 0.02774 | 0.02819 | 2.477 | 0.9524 ± 0.053 | 0.4762 |
| 100 | threads+pool | 4 | 0.0349 ± 0.0037 | 0.03198 | 0.03383 | 10.67 | 0.7752 ± 0.091 | 0.1938 |
| 100 | threads (pool reutilizado) | 4 | 0.02938 ± 0.00084 | 0.02869 | 0.0291 | 2.865 | 0.9209 ± 0.052 | 0.2302 |
| 100 | threads+pool | 8 | 0.04199 ± 0.0037 | 0.03771 | 0.04235 | 8.916 | 0.6444 ± 0.066 | 0.08055 |
| 100 | threads (pool reutilizado) | 8 | 0.03224 ± 0.0049 | 0.02915 | 0.03033 | 15.17 | 0.8392 ± 0.13 | 0.1049 |
| 100 | threads+pool | 12 | 0.06104 ± 0.0091 | 0.04502 | 0.0628 | 14.83 | 0.4433 ± 0.069 | 0.03694 |
| 100 | threads (pool reutilizado) | 12 | 0.03188 ± 0.0029 | 0.02909 | 0.03048 | 9.12 | 0.8488 ± 0.088 | 0.07073 |
| 100 | procesos+pool | 1 | 0.07622 ± 0.0017 | 0.07301 | 0.0763 | 2.267 | 0.355 ± 0.019 | 0.355 |
| 100 | procesos (pool reutilizado) | 1 | 0.02879 ± 0.0027 | 0.02717 | 0.02771 | 9.541 | 0.9397 ± 0.1 | 0.9397 |
| 100 | procesos+pool | 2 | 0.102 ± 0.0022 | 0.09996 | 0.101 | 2.164 | 0.2652 ± 0.014 | 0.1326 |
| 100 | procesos (pool reutilizado) | 2 | 0.01636 ± 0.001 | 0.01529 | 0.01595 | 6.182 | 1.654 ± 0.13 | 0.8268 |
| 100 | procesos+pool | 4 | 0.1839 ± 0.0042 | 0.1782 | 0.1842 | 2.272 | 0.1471 ± 0.008 | 0.03677 |
| 100 | procesos (pool reutilizado) | 4 | 0.01002 ± 0.0012 | 0.008975 | 0.009458 | 12.07 | 2.7 ± 0.35 | 0.675 |
| 100 | procesos+pool | 8 | 0.3091 ± 0.0038 | 0.3036 | 0.3088 | 1.237 | 0.08753 ± 0.0044 | 0.01094 |
| 100 | procesos (pool reutilizado) | 8 | 0.008139 ± 0.0015 | 0.00664 | 0.007659 | 17.92 | 3.324 ± 0.62 | 0.4156 |
| 100 | procesos+pool | 12 | 0.3966 ± 0.0039 | 0.3924 | 0.3963 | 0.977 | 0.06823 ± 0.0034 | 0.005686 |
| 100 | procesos (pool reutilizado) | 12 | 0.0117 ± 0.013 | 0.006665 | 0.007389 | 107.6 | 2.312 ± 2.5 | 0.1927 |

## N=1000, bloque=50

| n bloques | config | p | t (s) | min | mediana | CV% | speedup | efic. |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 400 | secuencial por bloques (base) | 1 | 0.02799 ± 0.00063 | 0.02745 | 0.0278 | 2.245 | 1 ± 0 | 1 |
| 400 | procesos (pool reutilizado) | 12 | 0.01212 ± 0.013 | 0.006717 | 0.008053 | 107.2 | 2.309 ± 2.5 | 0.1924 |

## N=1000, bloque=200

| n bloques | config | p | t (s) | min | mediana | CV% | speedup | efic. |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 25 | secuencial por bloques (base) | 1 | 0.02648 ± 0.0003 | 0.02618 | 0.02639 | 1.127 | 1 ± 0 | 1 |
| 25 | procesos (pool reutilizado) | 12 | 0.01988 ± 0.027 | 0.006007 | 0.0086 | 136.4 | 1.332 ± 1.8 | 0.111 |

## N=1000, bloque=500

| n bloques | config | p | t (s) | min | mediana | CV% | speedup | efic. |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | secuencial por bloques (base) | 1 | 0.02607 ± 0.00023 | 0.0256 | 0.02612 | 0.8703 | 1 ± 0 | 1 |
| 4 | procesos (pool reutilizado) | 12 | 0.01017 ± 0.0015 | 0.008328 | 0.01032 | 14.89 | 2.564 ± 0.38 | 0.2137 |

## Notas

- Los '±' son la desviacion estandar muestral (ddof=1) de las corridas individuales; '-' si hubo una sola corrida.
- Semilla=42, reps=[10] (+1 warmup descartado).
- '+pool' incluye la creacion del pool en cada medicion (con procesos, el arranque de los workers; con forkserver cada worker reimporta el modulo, numpy incluido); '(pool reutilizado)' no.
- Los bloques se generan fuera de la region cronometrada. En el barrido de bloque, con bloque=500 solo hay 4 bloques para 12 workers, lo que limita el paralelismo.
- Speedup respecto a la suma secuencial sobre los mismos bloques (sec_bloques); el bucle plano es solo referencia.
- Todos los resultados se verifican contra la suma secuencial (RuntimeError si difieren).
