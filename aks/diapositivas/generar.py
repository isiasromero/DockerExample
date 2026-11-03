# Genera las diapositivas 1920x1080 del video de AKS (HTML -> PNG con Chrome headless).
# Uso: python aks/diapositivas/generar.py   (deja los PNG en C:\Users\isias\Videos\aks-tutorial\diapositivas)
import pathlib, subprocess, sys

AQUI = pathlib.Path(__file__).parent
SALIDA = pathlib.Path(r"C:\Users\isias\Videos\aks-tutorial\diapositivas")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PIE_IZQ = "Contenerización de Aplicaciones de Software · Unidad 3"
PIE_DER = "Azure Kubernetes Service"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=block');
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1920px;height:1080px;overflow:hidden}
body{font-family:Inter,sans-serif;color:#e8edf7;background:#0b1220;position:relative;
 background-image:radial-gradient(ellipse 1100px 520px at 1700px -60px,#14284e 0%,rgba(11,18,32,0) 70%)}
.marco{position:absolute;inset:110px 140px 120px 140px;display:flex;flex-direction:column}
.ceja{color:#5b9cff;font-weight:700;letter-spacing:.32em;font-size:26px;text-transform:uppercase}
h1{font-size:84px;font-weight:800;letter-spacing:-.035em;line-height:1.05;margin-top:22px}
.pie{position:absolute;left:140px;right:140px;bottom:52px;display:flex;justify-content:space-between;color:#6b7a96;font-size:24px}
.cuerpo{flex:1;display:flex;align-items:center}
.caja{background:#111b2e;border:2px solid #22304a;border-radius:22px;padding:30px 34px}
.azul{border-color:#2f6fe4}.verde{border-color:#2fbf71}.ambar{border-color:#f0b84a}.rojo{border-color:#e5605b}
.t{font-weight:700;font-size:36px}.s{color:#9aa8c2;font-size:27px;line-height:1.45;margin-top:10px}
code,.mono{font-family:'JetBrains Mono',monospace}
.chip{display:inline-block;background:#16233b;border:1px solid #2a3a58;border-radius:12px;padding:12px 20px;font-size:26px;margin:7px 6px 0 0}
ul{list-style:none}li{position:relative;padding-left:34px;font-size:29px;line-height:1.4;margin:16px 0;color:#d5ddec}
li:before{content:'';position:absolute;left:4px;top:15px;width:12px;height:12px;border-radius:3px;background:var(--c,#5b9cff)}
"""

def pagina(cuerpo, ceja="", titulo="", pie=True):
    cab = f'<div class="ceja">{ceja}</div><h1>{titulo}</h1>' if titulo else ""
    p = f'<div class="pie"><span>{PIE_IZQ}</span><span>{PIE_DER}</span></div>' if pie else ""
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="marco">{cab}{cuerpo}</div>{p}</body></html>'

D = {}

D["00-portada"] = pagina("""
<div style="flex:1;display:flex;flex-direction:column;justify-content:center">
 <div class="ceja">Unidad 3 · Kubernetes en la nube</div>
 <h1 style="font-size:120px;margin-top:26px">Azure Kubernetes<br>Service (AKS)</h1>
 <div style="font-size:44px;color:#8fa0c0;margin-top:34px;line-height:1.35">Características, ventajas y desventajas,<br>y el despliegue de dos aplicaciones en un clúster real</div>
 <div style="display:flex;gap:30px;margin-top:60px">
  <svg width="110" height="64"><rect x="3" y="3" width="104" height="58" rx="9" fill="#2f6fe4"/><g stroke="#7fb0ff" stroke-width="3"><line x1="20" y1="12" x2="20" y2="52"/><line x1="36" y1="12" x2="36" y2="52"/><line x1="52" y1="12" x2="52" y2="52"/><line x1="68" y1="12" x2="68" y2="52"/><line x1="84" y1="12" x2="84" y2="52"/></g></svg>
  <svg width="110" height="64"><rect x="3" y="3" width="104" height="58" rx="9" fill="#2fbf71"/><g stroke="#8fe6b5" stroke-width="3"><line x1="20" y1="12" x2="20" y2="52"/><line x1="36" y1="12" x2="36" y2="52"/><line x1="52" y1="12" x2="52" y2="52"/><line x1="68" y1="12" x2="68" y2="52"/><line x1="84" y1="12" x2="84" y2="52"/></g></svg>
  <svg width="64" height="64" viewBox="0 0 64 64"><polygon points="32,3 57,17 57,47 32,61 7,47 7,17" fill="none" stroke="#f0b84a" stroke-width="4"/><circle cx="32" cy="32" r="8" fill="#f0b84a"/></svg>
 </div>
</div>""", pie=False).replace("</body>", '<div class="pie"><span>Contenerización de Aplicaciones de Software · Politécnico Grancolombiano</span><span>Microsoft Azure</span></div></body>')

D["01-que-es-kubernetes"] = pagina("""
<div class="cuerpo" style="gap:44px;align-items:center;margin-top:40px;margin-bottom:40px">
 <div class="caja azul" style="flex:1">
  <div class="t">Plano de control</div><div class="s">Toma las decisiones del clúster</div>
  <div style="margin-top:22px"><span class="chip">API server</span><span class="chip">etcd</span><span class="chip">scheduler</span><span class="chip">controller manager</span></div>
  <div class="s" style="margin-top:34px;color:#7fb0ff">En AKS lo opera Azure</div>
 </div>
 <div style="display:flex;align-items:center;font-size:64px;color:#5b9cff">→</div>
 <div style="flex:1.25;display:flex;flex-direction:column;gap:26px">
  <div class="caja verde"><div class="t">Nodo 1</div><div style="margin-top:8px"><span class="chip">kubelet</span><span class="chip">pod</span><span class="chip">pod</span><span class="chip">pod</span></div></div>
  <div class="caja verde"><div class="t">Nodo 2</div><div style="margin-top:8px"><span class="chip">kubelet</span><span class="chip">pod</span><span class="chip">pod</span></div></div>
  <div class="s" style="margin-top:0;color:#7ee0a8">Ejecutan los contenedores de nuestras aplicaciones</div>
 </div>
</div>
<div class="s" style="font-size:30px">Se declara el <b style="color:#fff">estado deseado</b> (por ejemplo, 3 réplicas) y Kubernetes trabaja para mantenerlo.</div>
""", "Kubernetes", "Plano de control y nodos")

D["02-que-hace-azure"] = pagina("""
<div class="cuerpo" style="gap:50px">
 <div class="caja azul" style="flex:1;padding:40px 44px"><div class="t" style="color:#7fb0ff">Azure administra</div>
  <ul style="margin-top:14px"><li>Plano de control disponible</li><li>Actualizaciones de Kubernetes</li><li>Parches de seguridad</li><li>Integración con red, discos e identidad</li></ul></div>
 <div class="caja verde" style="flex:1;padding:40px 44px"><div class="t" style="color:#7ee0a8">Nosotros administramos</div>
  <ul style="margin-top:14px;--c:#2fbf71"><li>Los nodos (tamaño y cantidad)</li><li>Las imágenes de contenedor</li><li>Los manifiestos de las aplicaciones</li><li>Los costos de los recursos</li></ul></div>
</div>
""", "Qué es AKS", "Kubernetes administrado")

def tarjeta(color, titulo, texto):
    return f'<div class="caja {color}" style="padding:30px 34px"><div class="t" style="font-size:34px">{titulo}</div><div class="s" style="font-size:26px">{texto}</div></div>'

D["03-caracteristicas"] = pagina(f"""
<div style="flex:1;display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-top:56px">
 {tarjeta("azul","Niveles Free, Standard y Premium","En Free el plano de control no cuesta; Standard y Premium agregan acuerdo de nivel de servicio (SLA).")}
 {tarjeta("verde","Integrado con Azure","Container Registry, Microsoft Entra ID, discos administrados, balanceadores de carga y Azure Monitor.")}
 {tarjeta("ambar","Un solo comando","<code>az aks create</code> crea el clúster con el registro de imágenes ya conectado.")}
 {tarjeta("azul","Automatización","Escalado automático de nodos y AKS Automatic, que aplica buenas prácticas por defecto.")}
</div>
""", "Características", "Lo que diferencia a AKS")

D["04-ventajas-desventajas"] = pagina("""
<div class="cuerpo" style="gap:44px;align-items:center;margin-top:20px">
 <div class="caja verde" style="flex:1;padding:36px 42px"><div class="t" style="color:#7ee0a8">Ventajas</div>
  <ul style="--c:#2fbf71"><li>Menos carga operativa: Azure opera el plano de control</li><li>Integración nativa con identidad, monitoreo y almacenamiento</li><li>Manifiestos estándar, portables a otros proveedores</li><li>Plano de control gratis en el nivel Free</li></ul></div>
 <div class="caja rojo" style="flex:1;padding:36px 42px"><div class="t" style="color:#ff8f8a">Desventajas</div>
  <ul style="--c:#e5605b"><li>Nivel Free sin SLA: no apto para producción</li><li>Nodos, discos, IP y registros se pagan aunque estén ociosos</li><li>Dependencia del proveedor en los servicios integrados</li><li>La complejidad de Kubernetes no desaparece</li><li>Cuentas de estudiante con cupos bajos de CPU</li></ul></div>
</div>
""", "Balance", "Ventajas y desventajas")

filas = [("services: web", "Deployment (2 réplicas)"), ("services: db", "StatefulSet"),
         ("volumes", "PersistentVolumeClaim → disco de Azure"), ("environment", "ConfigMap"),
         ("contraseñas", "Secret"), ("healthcheck", "readiness / liveness probes"), ("ports", "Service LoadBalancer → IP pública")]
tabla = "".join(f'<div class="mono" style="color:#f0b84a;font-size:30px;padding:16px 0;border-bottom:1px solid #1e2a42">{a}</div><div style="color:#5b9cff;font-size:34px;text-align:center;padding:12px 0;border-bottom:1px solid #1e2a42">→</div><div style="font-size:30px;padding:16px 0;border-bottom:1px solid #1e2a42">{b}</div>' for a, b in filas)
D["05-compose-a-kubernetes"] = pagina(f"""
<div style="display:grid;grid-template-columns:1fr 120px 1.6fr;margin-top:56px">
 <div class="ceja" style="color:#9aa8c2;letter-spacing:.2em;font-size:22px;padding-bottom:10px">Docker Compose</div><div></div><div class="ceja" style="color:#9aa8c2;letter-spacing:.2em;font-size:22px;padding-bottom:10px">Kubernetes</div>
 {tabla}
</div>
""", "De la Unidad 2 a la 3", "Docker Compose → Kubernetes")

D["06-dos-aplicaciones"] = pagina("""
<div class="cuerpo" style="gap:44px;align-items:stretch;margin-top:56px">
 <div class="caja azul" style="flex:1;padding:38px 42px"><div class="ceja" style="font-size:20px">Aplicación 1 · con estado</div><div class="t" style="font-size:44px;margin-top:12px">Tienda Node.js + MySQL</div>
  <div style="margin-top:22px"><span class="chip">namespace tienda</span><span class="chip">ConfigMap</span><span class="chip">Secret</span><span class="chip">StatefulSet + PVC</span><span class="chip">Deployment ×2</span><span class="chip">LoadBalancer</span><span class="chip">probes</span></div>
  <div class="s" style="margin-top:26px">Imágenes propias en Azure Container Registry. Los datos viven en un disco administrado.</div></div>
 <div class="caja verde" style="flex:1;padding:38px 42px"><div class="ceja" style="font-size:20px;color:#2fbf71">Aplicación 2 · sin estado</div><div class="t" style="font-size:44px;margin-top:12px">whoami</div>
  <div style="margin-top:22px"><span class="chip">namespace whoami</span><span class="chip">Deployment ×3</span><span class="chip">LoadBalancer</span><span class="chip">HPA</span></div>
  <div class="s" style="margin-top:26px">Responde con el nombre del pod que atiende cada petición: así se ve el balanceo de carga.</div></div>
</div>
<div class="s" style="font-size:28px">Un clúster Free con 2 nodos <code>Standard_B2as_v2</code>, creado con <code>az aks create</code>.</div>
""", "La demostración", "Dos aplicaciones, un clúster")

D["07-conclusiones"] = pagina("""
<div class="cuerpo"><ul style="max-width:1500px">
 <li style="font-size:36px;margin:26px 0">AKS reduce el trabajo de operar Kubernetes: Azure se encarga del plano de control.</li>
 <li style="font-size:36px;margin:26px 0;--c:#2fbf71">Se integra con el registro, los discos, la red y la identidad de Azure.</li>
 <li style="font-size:36px;margin:26px 0;--c:#f0b84a">Exige vigilar los costos y entender bien los objetos de Kubernetes.</li>
 <li style="font-size:36px;margin:26px 0;--c:#e5605b">Al terminar, <code>az group delete</code> borra todo para no consumir crédito.</li>
</ul></div>
""", "Cierre", "Conclusiones")

refs = [
 "Burns, B., Grant, B., Oppenheimer, D., Brewer, E. y Wilkes, J. (2016). Borg, Omega, and Kubernetes. <i>ACM Queue, 14</i>(1), 70–93. https://doi.org/10.1145/2898442.2898444",
 "Microsoft. (s.f.-a). <i>Free, Standard, and Premium pricing tiers for AKS cluster management</i>. Microsoft Learn. https://learn.microsoft.com/azure/aks/free-standard-pricing-tiers",
 "Microsoft. (s.f.-b). <i>What is Azure Kubernetes Service (AKS)?</i> Microsoft Learn. https://learn.microsoft.com/azure/aks/what-is-aks",
 "The Kubernetes Authors. (s.f.). <i>Kubernetes documentation</i>. https://kubernetes.io/docs/",
]
D["08-referencias"] = pagina('<div style="margin-top:60px">' + "".join(
    f'<p style="font-size:28px;line-height:1.5;color:#d5ddec;margin:0 0 30px;padding-left:56px;text-indent:-56px">{r}</p>' for r in refs) + "</div>",
    "Fuentes", "Referencias")

def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    html_dir = AQUI / "html"; html_dir.mkdir(exist_ok=True)
    solo = sys.argv[1:]
    for nombre, html in D.items():
        if solo and nombre not in solo: continue
        f = html_dir / f"{nombre}.html"; f.write_text(html, encoding="utf-8")
        png = SALIDA / f"{nombre}.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--window-size=1920,1080", "--virtual-time-budget=5000", f"--screenshot={png}", f.as_uri()],
                       check=True, capture_output=True)
        print(png)

if __name__ == "__main__":
    main()
