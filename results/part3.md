# Parte 3: SMP + SIMD

## Sistema

- Python: 3.14.7
- Build free-threaded (Py_GIL_DISABLED): False
- GIL habilitado: True
- CPUs logicas: 12
- NumPy: 2.5.3
- Plataforma: Linux-7.2.4-arch1-2-x86_64-with-glibc2.44
- Fecha: 2026-10-08T17:58:04

## N=10000, bloque=1000

| config | p | t (s) | min | mediana | CV% | speedup | efic. | GB/s |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| secuencial NumPy (bloques) | 1 | 0.04339 ± 0.00025 | 0.04295 | 0.04344 | 0.58 | 1 ± 0 | 1 | 9.219 |
| mat.sum() directo | 1 | 0.03451 ± 0.0004 | 0.03424 | 0.03434 | 1.152 | 1.257 ± 0.016 | 1.257 | 11.59 |
| Python puro (ESTIMADO) | 1 | 3.161 ± 0.013 | 3.147 | 3.161 | 0.4154 | - | - | - |
| threads | 1 | 0.0466 ± 0.0011 | 0.04536 | 0.04627 | 2.31 | 0.931 ± 0.022 | 0.931 | 8.583 |
| threads | 2 | 0.02685 ± 0.00042 | 0.02625 | 0.02694 | 1.567 | 1.616 ± 0.027 | 0.8081 | 14.9 |
| threads | 4 | 0.01736 ± 0.00037 | 0.0168 | 0.01734 | 2.113 | 2.5 ± 0.055 | 0.6249 | 23.04 |
| threads | 8 | 0.01542 ± 0.00027 | 0.01497 | 0.01539 | 1.782 | 2.813 ± 0.053 | 0.3517 | 25.94 |
| threads | 12 | 0.01501 ± 0.00046 | 0.01439 | 0.01502 | 3.076 | 2.89 ± 0.09 | 0.2408 | 26.64 |
| procesos (bloque como argumento) | 1 | 0.5355 ± 0.0056 | 0.5239 | 0.5347 | 1.043 | 0.08102 ± 0.00097 | 0.08102 | 0.7469 |
| procesos (bloque como argumento) | 2 | 0.4059 ± 0.0068 | 0.3977 | 0.4041 | 1.687 | 0.1069 ± 0.0019 | 0.05344 | 0.9854 |
| procesos (bloque como argumento) | 4 | 0.414 ± 0.0047 | 0.4049 | 0.4134 | 1.145 | 0.1048 ± 0.0013 | 0.0262 | 0.9663 |
| procesos (bloque como argumento) | 8 | 0.4174 ± 0.0098 | 0.4007 | 0.4162 | 2.338 | 0.104 ± 0.0025 | 0.013 | 0.9584 |
| procesos (bloque como argumento) | 12 | 0.4153 ± 0.0072 | 0.4024 | 0.4167 | 1.741 | 0.1045 ± 0.0019 | 0.008708 | 0.9633 |

## Notas

- Los '±' son la desviacion estandar muestral (ddof=1) de las corridas individuales; '-' si hubo una sola corrida.
- int32, semilla=42, reps=[3, 10] (+1 warmup descartado).
- Pools creados una vez por configuracion fuera de la region cronometrada; el arranque de los workers queda fuera del tiempo.
- Procesos: cada bloque se copia y se envia como argumento (pickle); copia y serializacion estan incluidas en el tiempo. Solo concurrent.futures.
- GB/s = bytes de la matriz / tiempo (ancho de banda efectivo de lectura).
- Python puro: ESTIMADO por extrapolacion de un bloque; no medido, sin speedup.
