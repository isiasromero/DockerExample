# Genera un mp3 por tramo del plan con ElevenLabs (voz costena, modelo v3). Clave en ELEVENLABS_API_KEY.
# Uso: python aks/montaje/voz.py [id ...]   (sin ids genera los que falten)
import os, re, sys, json, time, pathlib, subprocess, requests
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from plan import TRAMOS, FONETICA

VOZ, MODELO = "8BVnD625pACRJOqMoMoJ", "eleven_v3"
AJUSTES = {"stability": 0.5, "similarity_boost": 0.95, "style": 0.0}
ACENTO = "[acento colombiano costeño, de la costa caribe] "
SALIDA = pathlib.Path(r"C:\Users\isias\Videos\aks-tutorial\voz2")

def fon(t):
    for a, b in FONETICA:
        t = re.sub(rf"(?<![\w]){re.escape(a)}(?![\w])", b, t)
    return t

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).strip())

def generar(tid, texto, intento=0):
    out = SALIDA / f"{tid}.mp3"
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}?output_format=mp3_44100_192",
                      headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]},
                      json={"text": ACENTO + fon(texto), "model_id": MODELO, "voice_settings": AJUSTES, "language_code": "es"}, timeout=300)
    if r.status_code == 429 and intento < 6:  # el plan solo admite pocas peticiones simultaneas
        time.sleep(5 * (intento + 1)); return generar(tid, texto, intento + 1)
    if not r.ok:
        return tid, f"ERROR {r.status_code} {r.text[:150]}"
    out.write_bytes(r.content)
    return tid, round(dur(out), 2)

if __name__ == "__main__":
    SALIDA.mkdir(parents=True, exist_ok=True)
    pedidos = sys.argv[1:]
    trabajo = [(t, x) for t, _, x in TRAMOS if x and ((t in pedidos) if pedidos else not (SALIDA / f"{t}.mp3").exists())]
    with ThreadPoolExecutor(2) as ex:
        for tid, d in ex.map(lambda a: generar(*a), trabajo):
            print(tid, d)
    dur_json = {t: dur(SALIDA / f"{t}.mp3") for t, _, x in TRAMOS if x and (SALIDA / f"{t}.mp3").exists()}
    (SALIDA / "duraciones.json").write_text(json.dumps(dur_json, indent=1), encoding="utf-8")
    print("total voz:", round(sum(dur_json.values()), 1), "s")
