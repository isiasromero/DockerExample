# Graba una toma de la demo con ffmpeg (gdigrab): recuadro 16:9 de 1835x1032 arriba a la izquierda
# del monitor principal (sin la barra de tareas), escalado a 1920x1080.
# Uso: python aks/grabacion/grabar.py bloque N | tienda | whoami | vscode
import ctypes, os, pathlib, subprocess, sys, time

RAIZ = pathlib.Path(__file__).resolve().parents[2]
SALIDA = pathlib.Path(r"C:\Users\isias\Videos\aks-tutorial\tomas_asus")
MINTTY = r"C:\Program Files\Git\usr\bin\mintty.exe"
PW = r"C:\Users\isias\Documents\docker-app\grabacion\navegador\node_modules\playwright-core"
ANCHO, ALTO = 1920, 1080
X0, Y0 = -1920, 86  # monitor ASUS VZ239 a la izquierda del LG
user32 = ctypes.windll.user32

def ventana(titulo, espera=20, mover=True):
    """Busca una ventana visible cuyo titulo contenga `titulo` y la coloca en el recuadro de grabacion."""
    fin = time.time() + espera
    while time.time() < fin:
        hallada = []
        def cb(h, _):
            n = user32.GetWindowTextLengthW(h)
            if n and user32.IsWindowVisible(h):
                b = ctypes.create_unicode_buffer(n + 1); user32.GetWindowTextW(h, b, n + 1)
                if titulo in b.value: hallada.append(h)
            return True
        user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(cb), 0)
        if hallada:
            h = hallada[0]
            if mover: user32.ShowWindow(h, 9)  # restaurar antes de moverla (no a la terminal en pantalla completa)
            if mover:
                user32.MoveWindow(h, X0, Y0, ANCHO, ALTO, True); time.sleep(0.5); user32.ShowWindow(h, 3)  # maximizada en el ASUS
            user32.SetForegroundWindow(h)
            return h
        time.sleep(0.3)
    raise SystemExit(f"No aparecio la ventana '{titulo}'")

def rueda(clics):
    """Desplaza el editor con la rueda del mouse (negativo = hacia abajo), un clic cada 0.4 s."""
    user32.SetCursorPos(X0 + ANCHO // 2, Y0 + ALTO // 2)
    for _ in range(abs(clics)):
        user32.mouse_event(0x0800, 0, 0, 120 if clics > 0 else -120, 0); time.sleep(0.4)

def ip(ns, svc):
    return subprocess.check_output(["kubectl", "get", "svc", "-n", ns, svc, "-o",
                                    "jsonpath={.status.loadBalancer.ingress[0].ip}"], text=True).strip()

def grabar(destino):
    return subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "gdigrab", "-framerate", "30",
                             "-offset_x", str(X0), "-offset_y", str(Y0), "-video_size", f"{ANCHO}x{ALTO}", "-draw_mouse", "1",
                             "-i", "desktop", "-c:v", "libx264", "-preset", "veryfast",
                             "-crf", "18", "-pix_fmt", "yuv420p", str(destino)], stdin=subprocess.PIPE)

def main():
    tipo, arg = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "")
    nombre = {"bloque": f"bloque{arg}", "tienda": "navegador-tienda", "whoami": "navegador-whoami", "vscode": "vscode-manifiestos"}[tipo]
    SALIDA.mkdir(parents=True, exist_ok=True)
    destino = SALIDA / f"{nombre}.mp4"

    if tipo == "bloque":
        titulo = f"AKS demo bloque {arg}"
        proc = subprocess.Popen([MINTTY, "-p", f"{X0},{Y0}", "-w", "full", "-o", "FontHeight=15", "-o", "Font=Consolas",
               "-o", "BackgroundColour=12,12,12", "-o", "ForegroundColour=230,230,230", "-o", "Scrollbar=none",
               "-t", titulo, "--dir", str(RAIZ), "/bin/bash", "-l", "aks/grabacion/toma.sh", arg])
        h = ventana(titulo, mover=False); time.sleep(1)  # redimensionarla deja una imagen fantasma en gdigrab
        ff = grabar(destino)
        while user32.IsWindow(h): time.sleep(0.5)  # mintty se desliga: se espera a que cierre su ventana
    elif tipo in ("tienda", "whoami"):
        ns, svc = ("tienda", "tienda-web") if tipo == "tienda" else ("whoami", "whoami")
        ff = grabar(destino)
        subprocess.run(["node", str(RAIZ / "aks/grabacion/navegador.js"), tipo, ip(ns, svc)],
                       env=dict(os.environ, PW=PW, MONITOR_X=str(X0), MONITOR_Y=str(Y0), ANCHO=str(ANCHO), ALTO=str(ALTO)))
    else:
        # Muestra 03-mysql.yaml y 04-tienda-web.yaml, bajando despacio por cada uno
        code = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\bin\code.cmd")
        k8s = RAIZ / "aks/k8s"
        subprocess.run([code, "-n", str(k8s / "03-mysql.yaml")], shell=True)
        h = ventana("03-mysql.yaml", 40); time.sleep(6)
        ff = grabar(destino); time.sleep(10); rueda(-6); time.sleep(9)
        subprocess.run([code, "-r", str(k8s / "04-tienda-web.yaml")], shell=True)
        time.sleep(10); rueda(-5); time.sleep(9)
        user32.PostMessageW(ctypes.c_void_p(h), 0x10, 0, 0)  # WM_CLOSE
    time.sleep(1)
    ff.communicate(b"q", timeout=60)
    print(destino)

if __name__ == "__main__":
    main()
