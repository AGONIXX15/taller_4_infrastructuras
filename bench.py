import os
import sys

# BLAS con 1 hilo por defecto para aislar SIMD de SMP. Tiene que ir antes de importar numpy.
BLAS_MULTI = "--blas-hilos" in sys.argv
if not BLAS_MULTI:
    for var in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
                "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        os.environ[var] = "1"

import argparse
import datetime
import json
import math
import platform
import statistics
import sysconfig
import time

import numpy as np

import part1
import part2
import part3

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def leer_casos(ruta):
    return json.load(open(ruta))


def medir(fn, *args, reps=5, warmup=1):
    resultado = None
    for _ in range(warmup):
        resultado = fn(*args)
    tiempos = []
    for _ in range(reps):
        inicio = time.perf_counter()
        resultado = fn(*args)
        tiempos.append(time.perf_counter() - inicio)
    return resultado, tiempos


def resumen(tiempos):
    media = statistics.fmean(tiempos)
    desv = statistics.stdev(tiempos) if len(tiempos) > 1 else None
    return {
        "media": media,
        "desv": desv,
        "min": min(tiempos),
        "mediana": statistics.median(tiempos),
        "cv": 100 * desv / media if desv is not None and media else None,
    }


def speedup(base, tiempos, p):
    b, q = resumen(base), resumen(tiempos)
    s = b["media"] / q["media"]
    if b["desv"] is None or q["desv"] is None:
        s_std = None
    else:
        s_std = s * math.sqrt((b["desv"] / b["media"]) ** 2 + (q["desv"] / q["media"]) ** 2)
    return {"S": s, "S_std": s_std, "E": s / p}


def sin_gil():
    return not getattr(sys, "_is_gil_enabled", lambda: True)()


def celda(r, k):
    # k es una clave, o (media, desv) para mostrar "media ± desv"
    if isinstance(k, tuple):
        if r.get(k[0]) is None:
            return "-"
        return f"{r[k[0]]:.4g} ± " + ("-" if r.get(k[1]) is None else f"{r[k[1]]:.2g}")
    v = r.get(k)
    return "-" if v is None else f"{v:.4g}" if isinstance(v, float) else str(v)


def guardar(nombre, titulo, secciones, notas, tiempos, extra=()):
    # secciones: (titulo, filas, columnas). Escribe el md y los tiempos crudos en json.
    os.makedirs(RESULTS_DIR, exist_ok=True)
    sufijo = "_nogil" if sin_gil() else ""
    md = os.path.join(RESULTS_DIR, f"{nombre}{sufijo}.md")
    js = os.path.join(RESULTS_DIR, f"{nombre}_tiempos{sufijo}.json")
    info = [f"Python: {platform.python_version()}",
            f"GIL habilitado: {not sin_gil()}",
            f"Py_GIL_DISABLED: {bool(sysconfig.get_config_var('Py_GIL_DISABLED'))}",
            f"CPUs logicas: {os.cpu_count()}",
            f"NumPy: {np.__version__}",
            f"Fecha: {datetime.datetime.now().isoformat(timespec='seconds')}", *extra]
    notas = ["Los '±' son la desviacion estandar muestral (ddof=1); '-' si hubo una sola corrida."] + notas
    with open(md, "w") as f:
        f.write(f"# {titulo}\n\n## Sistema\n\n" + "".join(f"- {i}\n" for i in info))
        for t, filas, cols in secciones:
            f.write(f"\n## {t}\n\n| " + " | ".join(h for h, _ in cols) + " |\n")
            f.write("|" + "|".join("---:" for _ in cols) + "|\n")
            for r in filas:
                f.write("| " + " | ".join(celda(r, k) for _, k in cols) + " |\n")
        f.write("\n## Notas\n\n" + "".join(f"- {n}\n" for n in notas))
    json.dump(tiempos, open(js, "w"), indent=1)
    print(f"Guardado {md} y {js}")


# matriz de la parte actual; solo se guarda una para no gastar memoria
_cache = {}

def matriz(parte, n):
    if _cache.get("clave") != (parte, n):
        _cache.clear()
        if parte == 2:
            m = part2.generate_matrices(n)
        else:
            mod = part1 if parte == 1 else part3
            m = mod.generate_matrix(n)
            mod.init_worker(m)
        _cache["clave"] = (parte, n)
        _cache["mat"] = m
    return _cache["mat"]


def calentar(pool, p):
    # tareas bloqueantes para que existan los p workers antes de medir
    list(pool.map(time.sleep, [0.05] * p))


def correr1(c):
    mat = matriz(1, c["n"])
    b, reps, modo = c["bloque"], c["reps"], c["modo"]
    if modo == "secuencial":
        res, t = medir(part1.sec_bloques, part1.generate_blocks(mat, b), reps=reps)
        return "secuencial por bloques (base)", 1, res, t
    if modo == "plano":
        res, t = medir(part1.sec, mat, reps=reps)
        return "referencia: bucle plano sin bloques", 1, res, t
    p, proceso = c["workers"], modo == "procesos"
    blocks = part1.generate_blocks(mat, b)
    if c["pool"] == "nuevo":
        res, t = medir(part1.par, mat, blocks, proceso, p, reps=reps)
        return f"{modo}+pool", p, res, t
    with part1.crear_pool(proceso, mat, p) as pool:
        calentar(pool, p)
        res, t = medir(part1.run, pool, blocks, p, reps=reps)
    return f"{modo} (pool reutilizado)", p, res, t


def correr3(c):
    mat = matriz(3, c["n"])
    b, reps, modo = c["bloque"], c["reps"], c["modo"]
    blocks = part3.generate_blocks(mat, b)
    if modo == "secuencial":
        res, t = medir(part3.sec_blocks, blocks, reps=reps)
        return "secuencial NumPy (bloques)", 1, res, t
    if modo == "suma_directa":
        res, t = medir(lambda: int(mat.sum(dtype=np.int64)), reps=reps)
        return "mat.sum() directo", 1, res, t
    if modo == "python_estimado":
        # se mide un bloque y se extrapola al total
        sub = np.ascontiguousarray(mat[:b, :b])
        _, t = medir(part3.sec, sub, reps=reps)
        factor = (c["n"] * c["n"]) / (b * b)
        return "Python puro (ESTIMADO)", 1, None, [x * factor for x in t]
    p, proceso = c["workers"], modo == "procesos"
    with part3.crear_pool(proceso, mat, p) as pool:
        calentar(pool, p)
        if proceso:
            res, t = medir(part3.run_procesos, pool, mat, blocks, reps=reps)
            return "procesos (bloque como argumento)", p, res, t
        res, t = medir(part3.run, pool, blocks, p, reps=reps)
    return "threads", p, res, t


COLS = [
    ("config", "config"), ("p", "p"), ("t (s)", ("media", "desv")),
    ("min", "min"), ("mediana", "mediana"), ("CV%", "cv"),
    ("speedup", ("S", "S_std")), ("efic.", "E"),
]


def parte13(parte, casos):
    correr = correr1 if parte == 1 else correr3
    filas = []
    for c in casos:
        print(f"  {c['modo']} n={c['n']} bloque={c['bloque']} workers={c.get('workers', '-')} {c.get('pool', '')}", flush=True)
        config, p, res, t = correr(c)
        filas.append({"n": c["n"], "bloque": c["bloque"], "modo": c["modo"], "config": config, "p": p,
                      "n_bloques": math.ceil(c["n"] / c["bloque"]) ** 2,
                      **resumen(t), "_tiempos": t, "_resultado": res})
    # la base de cada grupo (n, bloque) es su caso secuencial
    bases = {(f["n"], f["bloque"]): f for f in filas if f["modo"] == "secuencial"}
    for f in filas:
        base = bases.get((f["n"], f["bloque"]))
        if base is None:
            raise RuntimeError(f"falta el caso secuencial para n={f['n']} bloque={f['bloque']}")
        f["gbs"] = None if f["modo"] == "python_estimado" else f["n"] ** 2 * 4 / f["media"] / 1e9
        if f["modo"] == "python_estimado":
            f.update(S=None, S_std=None, E=None)
            continue
        if f["_resultado"] != base["_resultado"]:
            raise RuntimeError(f"resultado distinto en {f['config']} p={f['p']}: {f['_resultado']} != {base['_resultado']}")
        if f is base:
            f.update(S=1.0, S_std=0.0 if len(f["_tiempos"]) > 1 else None, E=1.0)
        else:
            f.update(speedup(base["_tiempos"], f["_tiempos"], f["p"]))
    cols = ([("n bloques", "n_bloques")] + COLS) if parte == 1 else COLS + [("GB/s", "gbs")]
    grupos = {}
    for f in filas:
        grupos.setdefault((f["n"], f["bloque"]), []).append(f)
    secciones = [(f"N={n}, bloque={b}", rows, cols) for (n, b), rows in grupos.items()]
    reps = sorted({c["reps"] for c in casos})
    if parte == 1:
        notas = [f"Semilla={part1.SEED}, reps={reps} (+1 warmup). Base: suma secuencial por los mismos bloques.",
                 "'+pool' incluye crear el pool (y arrancar los procesos); '(pool reutilizado)' no."]
    else:
        notas = [f"int32, semilla={part3.SEED}, reps={reps} (+1 warmup). Base: NumPy secuencial por bloques.",
                 "Procesos: copia y pickle de cada bloque incluidos en el tiempo. Python puro es una estimacion (sin speedup)."]
    tiempos = [{k: f[k] for k in ("n", "bloque", "modo", "config", "p")} | {"tiempos": f["_tiempos"]} for f in filas]
    guardar(f"part{parte}", "Parte 1: SMP (Python puro)" if parte == 1 else "Parte 3: SMP + SIMD",
            secciones, notas, tiempos)


def parte2(casos):
    datos = {}
    for c in casos:
        n, modo = c["n"], c["modo"]
        print(f"  {modo} n={n}", flush=True)
        a, b = matriz(2, n)
        if modo == "python":
            fn, args = part2.sec, (a.tolist(), b.tolist())
        elif modo == "numpy_int64":
            fn, args = part2.smp, (a, b)
        else:
            fn, args = part2.smp, (a.astype(np.float64), b.astype(np.float64))
        res, t = medir(fn, *args, reps=c["reps"], warmup=c.get("warmup", 1))
        datos.setdefault(n, {})[modo] = (res, t)

    rows = []
    for n, d in sorted(datos.items()):
        (res_py, t_py), (res_i, t_i), (res_f, t_f) = d["python"], d["numpy_int64"], d["numpy_float64"]
        if not np.array_equal(np.array(res_py, dtype=np.int64), res_i):
            raise RuntimeError(f"Python puro != NumPy int64 (N={n})")
        if not np.array_equal(res_f, res_i):
            raise RuntimeError(f"NumPy float64 != int64 (N={n})")
        py, ni, nf = resumen(t_py), resumen(t_i), resumen(t_f)
        rows.append({
            "N": n,
            "py_media": py["media"], "py_desv": py["desv"],
            "np_int_media": ni["media"], "np_int_desv": ni["desv"],
            "np_f64_media": nf["media"], "np_f64_desv": nf["desv"],
            "speedup_int": py["media"] / ni["media"], "speedup_f64": py["media"] / nf["media"],
            "gflops_f64": 2 * n ** 3 / nf["media"] / 1e9,
        })
    cols = [
        ("N", "N"), ("t Python (s)", ("py_media", "py_desv")),
        ("t NumPy int64 (s)", ("np_int_media", "np_int_desv")),
        ("t NumPy f64 (s)", ("np_f64_media", "np_f64_desv")),
        ("speedup int64", "speedup_int"), ("speedup f64", "speedup_f64"),
        ("GFLOP/s f64", "gflops_f64"),
    ]
    modo = "multihilo" if BLAS_MULTI else "1 hilo"
    notas = [f"Semilla={part2.SEED}, reps={sorted({c['reps'] for c in casos})}, warmup=1 (0 en Python puro con n>=500)."]
    tiempos = [{"n": n, "modo": m, "tiempos": v[1]} for n, d in sorted(datos.items()) for m, v in d.items()]
    guardar("part2_blas_multi" if BLAS_MULTI else "part2", "Parte 2: SIMD (NumPy vs bucle triple)",
            [("Multiplicacion de matrices", rows, cols)], notas, tiempos, [f"Modo BLAS: {modo}"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Corre los casos de un archivo json")
    ap.add_argument("casos", help="archivo generado por casos.py")
    ap.add_argument("--blas-hilos", action="store_true", help="BLAS con varios hilos (parte 2)")
    casos = leer_casos(ap.parse_args().casos)
    print(f"Python {platform.python_version()}, GIL {'desactivado' if sin_gil() else 'activo'}, {len(casos)} casos")
    for parte in (1, 2, 3):
        grupo = [c for c in casos if c["parte"] == parte]
        if grupo:
            print(f"\n=== parte {parte}")
            parte2(grupo) if parte == 2 else parte13(parte, grupo)
