# Encuentra en cada toma de terminal el segundo en que aparece cada comentario verde de la demo (OCR de Windows).
# Uso: python aks/grabacion/marcas_ocr.py  -> escribe marcas.json junto a las tomas
import asyncio, difflib, json, pathlib, re, subprocess, tempfile
from concurrent.futures import ProcessPoolExecutor

RAIZ = pathlib.Path(__file__).resolve().parents[2]
TOMAS = pathlib.Path(r"C:\Users\isias\Videos\aks-tutorial\tomas_asus")
PASO = 1.0  # segundos entre fotogramas

def pasos_por_bloque():
    bloques, actual = {}, None
    for l in (RAIZ / "aks/scripts/02-demo-grabacion.sh").read_text(encoding="utf-8").splitlines():
        m = re.search(r'B == (\d)', l)
        if m: actual = m.group(1); bloques[actual] = []
        m = re.match(r'\s*(titulo|paso) "([^"]+)"', l)
        if m and actual: bloques[actual].append(m.group(2))
    return bloques

def norm(t):
    return re.sub(r"[^a-z0-9 ]", "", t.lower()).strip()

async def ocr(motor, png):
    from winrt.windows.graphics.imaging import BitmapDecoder
    from winrt.windows.storage import StorageFile, FileAccessMode
    f = await StorageFile.get_file_from_path_async(png)
    s = await f.open_async(FileAccessMode.READ)
    bmp = await (await BitmapDecoder.create_async(s)).get_software_bitmap_async()
    return [l.text for l in (await motor.recognize_async(bmp)).lines]

async def marcar(b, textos):
    from winrt.windows.media.ocr import OcrEngine
    from winrt.windows.globalization import Language
    motor = OcrEngine.try_create_from_language(Language("es-MX"))
    tmp = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(TOMAS / f"bloque{b}.mp4"), "-vf", f"fps={1/PASO}", str(tmp / "f%05d.png")], check=True)
    objetivos = [norm(t) for t in textos]
    hallados, sig = {}, 0  # los pasos aparecen en orden: solo se busca el siguiente
    for png in sorted(tmp.glob("f*.png")):
        if sig >= len(objetivos): break
        t = (int(png.stem[1:]) - 1) * PASO
        for linea in await ocr(motor, str(png)):
            n = norm(linea).lstrip("$ ")
            # se busca el siguiente paso; si el OCR no lo leyo pero ya aparece el de despues, se salta (queda None)
            for salto in (0, 1):
                k = sig + salto
                if k >= len(objetivos): break
                pref = objetivos[k][:25]
                if len(n) >= min(12, len(pref)) and (pref in n or difflib.SequenceMatcher(None, n[:len(pref) + 4], pref).ratio() > 0.85):
                    hallados[k] = t; sig = k + 1
                    break
            if sig >= len(objetivos): break
    return b, [{"texto": textos[i], "t": hallados.get(i)} for i in range(len(textos))]

def trabajo(args):
    return asyncio.run(marcar(*args))

if __name__ == "__main__":
    with ProcessPoolExecutor(5) as ex:
        marcas = dict(ex.map(trabajo, pasos_por_bloque().items()))
    for b, m in sorted(marcas.items()):
        print(b, [(x["t"], x["texto"][:28]) for x in m])
    (TOMAS / "marcas.json").write_text(json.dumps(marcas, ensure_ascii=False, indent=1), encoding="utf-8")
