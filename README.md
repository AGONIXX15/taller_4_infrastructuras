# Taller 4: SMP y SIMD en Python

Partes: `part1.py` (suma de matriz por bloques, Python puro), `part2.py` (multiplicacion de matrices, NumPy vs bucle triple), `part3.py` (suma por bloques con NumPy). Solo tienen los algoritmos; el benchmark esta en `bench.py`.

## Entornos

Dos venvs con el mismo numpy, uno con GIL y otro free-threaded:

    uv venv .venv-gil --python /usr/bin/python3.14 && uv pip install --python .venv-gil/bin/python numpy==2.5.3
    uv python install 3.14.7+freethreaded && uv venv .venv-ft --python 3.14.7+freethreaded && uv pip install --python .venv-ft/bin/python numpy==2.5.3

## Casos

    python casos.py            # escribe casos.json (suite completa)
    python casos.py --rapido   # escribe casos_rapido.json (tamanos chicos, para probar)

## Correr

    .venv-gil/bin/python bench.py casos.json
    .venv-ft/bin/python bench.py casos.json
    .venv-gil/bin/python bench.py casos.json --blas-hilos   # BLAS multihilo (parte 2)

Los resultados quedan en `results/` (csv y md). Con el interprete sin GIL los archivos llevan el sufijo `_nogil`, y con `--blas-hilos` la parte 2 lleva `_blas_multi`.
