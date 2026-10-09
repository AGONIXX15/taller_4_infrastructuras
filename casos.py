import json
import sys

# valores del suite completo y del rapido
CONFIG = {
    "completo": {"n1": 1000, "b1": 100, "bloques": [50, 100, 200, 500], "reps1": 10,
                 "n3": 10000, "b3": 1000, "reps3": 10,
                 "workers": [1, 2, 4, 8, 12],
                 "tamanos": [100, 200, 300, 500, 1000], "reps_py": 5, "reps_np": 20},
    "rapido": {"n1": 500, "b1": 100, "bloques": [50, 100, 250], "reps1": 3,
               "n3": 4000, "b3": 400, "reps3": 3,
               "workers": [1, 2, 4],
               "tamanos": [100, 200], "reps_py": 2, "reps_np": 5},
}


def armar(cfg):
    casos = []

    n, b, reps = cfg["n1"], cfg["b1"], cfg["reps1"]
    casos.append({"parte": 1, "n": n, "bloque": b, "modo": "secuencial", "reps": reps})
    casos.append({"parte": 1, "n": n, "bloque": b, "modo": "plano", "reps": reps})
    for modo in ("threads", "procesos"):
        for p in cfg["workers"]:
            for pool in ("nuevo", "reutilizado"):
                casos.append({"parte": 1, "n": n, "bloque": b, "modo": modo,
                              "workers": p, "pool": pool, "reps": reps})
    # tamano de bloque, procesos con el maximo de workers
    for bs in cfg["bloques"]:
        seq = {"parte": 1, "n": n, "bloque": bs, "modo": "secuencial", "reps": reps}
        par = {"parte": 1, "n": n, "bloque": bs, "modo": "procesos",
               "workers": max(cfg["workers"]), "pool": "reutilizado", "reps": reps}
        for c in (seq, par):
            if c not in casos:
                casos.append(c)

    for n in cfg["tamanos"]:
        warmup = 1 if n < 500 else 0
        reps = cfg["reps_py"] if n < 1000 else min(3, cfg["reps_py"])
        casos.append({"parte": 2, "n": n, "modo": "python", "reps": reps, "warmup": warmup})
        casos.append({"parte": 2, "n": n, "modo": "numpy_int64", "reps": cfg["reps_np"]})
        casos.append({"parte": 2, "n": n, "modo": "numpy_float64", "reps": cfg["reps_np"]})

    n, b, reps = cfg["n3"], cfg["b3"], cfg["reps3"]
    casos.append({"parte": 3, "n": n, "bloque": b, "modo": "secuencial", "reps": reps})
    casos.append({"parte": 3, "n": n, "bloque": b, "modo": "suma_directa", "reps": reps})
    casos.append({"parte": 3, "n": n, "bloque": b, "modo": "python_estimado", "reps": 3})
    for modo in ("threads", "procesos"):
        for p in cfg["workers"]:
            casos.append({"parte": 3, "n": n, "bloque": b, "modo": modo, "workers": p, "reps": reps})
    return casos


if __name__ == "__main__":
    rapido = "--rapido" in sys.argv
    archivo = "casos_rapido.json" if rapido else "casos.json"
    casos = armar(CONFIG["rapido" if rapido else "completo"])
    with open(archivo, "w") as f:
        json.dump(casos, f, indent=1)
    print(f"{len(casos)} casos en {archivo}")
