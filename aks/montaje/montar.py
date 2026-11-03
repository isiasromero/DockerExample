# Arma el video final: diapositivas + tomas (aceleradas o congeladas segun la locucion de cada tramo) + voz.
# Uso: python aks/montaje/montar.py [--calcular]   (--calcular solo muestra la duracion estimada)
import json, pathlib, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from plan import TRAMOS

BASE = pathlib.Path(r"C:\Users\isias\Videos\aks-tutorial")
DIAP, TOMAS, VOZ, TMP = BASE / "diapositivas", BASE / "tomas_asus", BASE / "voz2", BASE / "montaje"
FINAL = BASE / "video_final_aks.mp4"
ANTES, DESPUES = 0.4, 0.8      # respiro antes y despues de cada locucion (sin huecos largos)
SMAX = float(next((a.split("=")[1] for a in sys.argv if a.startswith("--smax=")), 2.6))
RECORTE_FIN = {"bloque": 2.0, "navegador": 1.2, "vscode": 1.0}  # quita el cierre de la ventana

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).strip())

DV = json.loads((VOZ / "duraciones.json").read_text(encoding="utf-8"))
DT = {p.stem: dur(p) for p in TOMAS.glob("*.mp4")}
MARCAS = json.loads((TOMAS / "marcas.json").read_text(encoding="utf-8"))

def paso(toma, k):
    """Segundo en que aparece el comentario verde k del bloque (0 = inicio de la toma)."""
    if k == 0: return 0.0
    t = MARCAS[toma[-1]][k]["t"]
    if t is None: raise SystemExit(f"Falta la marca {k} de {toma}: revisa marcas.json")
    return float(t)

def calcular(tid, visual, texto):
    v = DV.get(tid, 0.0)
    objetivo = (ANTES + v + DESPUES) if texto else 9.0
    if tid == "s01": objetivo += 1.0
    if tid == TRAMOS[-1][0]: objetivo = max(objetivo, 9.0)  # tiempo para leer las referencias
    if visual[0] == "img":
        return {"tid": tid, "tipo": "img", "img": visual[1], "salida": objetivo, "voz": v}
    _, toma, a, b = visual
    if isinstance(a, tuple): a = paso(toma, a[1])
    if isinstance(b, tuple): b = paso(toma, b[1])
    if b is None:
        b = DT[toma] - next(r for k, r in RECORTE_FIN.items() if toma.startswith(k))
    largo = b - a
    vel = 1.0 if largo <= objetivo else min(largo / objetivo, SMAX)
    salida = max(largo / vel, objetivo)
    return {"tid": tid, "tipo": "vid", "toma": toma, "a": a, "b": b, "vel": vel, "salida": salida, "voz": v}

def clip(c):
    out = TMP / f"{c['tid']}.mp4"
    voz = VOZ / f"{c['tid']}.mp3"
    T = c["salida"]
    if c["tipo"] == "img":
        entrada = ["-loop", "1", "-framerate", "30", "-t", f"{T:.3f}", "-i", str(DIAP / f"{c['img']}.png")]
        vf = "scale=1920:1080,format=yuv420p"
    else:
        entrada = ["-ss", f"{c['a']:.3f}", "-to", f"{c['b']:.3f}", "-i", str(TOMAS / f"{c['toma']}.mp4")]
        vf = f"setpts=(PTS-STARTPTS)/{c['vel']:.4f},fps=30,tpad=stop_mode=clone:stop_duration=60,trim=duration={T:.3f},format=yuv420p"
    if c["tid"] == "s01": vf += ",fade=t=in:st=0:d=0.8"
    if c["tid"] == TRAMOS[-1][0]: vf += f",fade=t=out:st={T - 1.2:.3f}:d=1.2"
    if c["voz"]:
        audio = ["-i", str(voz)]
        inicio = ANTES + (1.0 if c["tid"] == "s01" else 0)
        if c["tipo"] == "vid" and T - c["voz"] - ANTES - DESPUES > 1.0:
            # sobra tiempo: la pausa queda mientras se escribe el comando y la voz termina con el resultado en pantalla
            inicio = T - DESPUES - c["voz"]
        retardo = int(inicio * 1000)
        af = ["-filter_complex", f"[1:a]adelay={retardo}|{retardo},apad,atrim=duration={T:.3f},aresample=48000[a]", "-map", "0:v", "-map", "[a]"]
    else:
        audio = ["-f", "lavfi", "-t", f"{T:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
        af = ["-map", "0:v", "-map", "1:a"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *entrada, *audio, "-vf", vf, *af, "-t", f"{T:.3f}",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ac", "2", str(out)], check=True)
    return out

def main():
    plan = [calcular(*t) for t in TRAMOS]
    total = sum(c["salida"] for c in plan)
    print(f"duracion estimada: {total/60:.2f} min (velocidad maxima {SMAX}x)")
    if "--calcular" in sys.argv:
        for c in plan: print(f"{c['tid']:4} {c['salida']:6.1f}s voz {c['voz']:5.1f}s vel {c.get('vel', 1):.2f}")
        return
    TMP.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(16) as ex:
        clips = list(ex.map(clip, plan))
    lista = TMP / "lista.txt"
    lista.write_text("".join(f"file '{p.as_posix()}'\n" for p in clips), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lista),
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "30",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(FINAL)], check=True)
    # marcas de tiempo de cada tramo, para verificar la sincronia
    t, filas = 0.0, []
    for c in plan:
        filas.append({"tid": c["tid"], "inicio": round(t, 2), "fin": round(t + c["salida"], 2)}); t += c["salida"]
    (BASE / "tramos.json").write_text(json.dumps(filas, indent=1), encoding="utf-8")
    print(FINAL, f"{dur(FINAL)/60:.2f} min")

if __name__ == "__main__":
    main()
