// Abre Edge maximizado en el monitor de grabacion y recorre las paginas de la demo.
// Uso: node navegador.js tienda <IP> | whoami <IP>
// Necesita playwright-core (se reutiliza el de ..\docker-app\grabacion\navegador).
const { chromium } = require(process.env.PW || 'playwright-core');
const http = require('http');
const [modo, ip] = process.argv.slice(2);
const X = process.env.MONITOR_X || '-1920';
const esperar = (ms) => new Promise((r) => setTimeout(r, ms));

const CURSOR = `(() => {
  const crear = () => { if (document.getElementById('__c')) return;
    const c = document.createElement('div'); c.id = '__c';
    c.innerHTML = '<svg width="26" height="26" viewBox="0 0 24 24"><path d="M4 2l16 10-7 1.5L10 21z" fill="#111" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/></svg>';
    Object.assign(c.style, {position:'fixed',left:'960px',top:'540px',zIndex:2147483647,pointerEvents:'none'});
    const p = JSON.parse(sessionStorage.getItem('__p') || 'null'); if (p) { c.style.left = p[0]+'px'; c.style.top = p[1]+'px'; }
    document.body.appendChild(c); };
  document.addEventListener('mousemove', (e) => { const c = document.getElementById('__c');
    if (c) { c.style.left = e.clientX+'px'; c.style.top = e.clientY+'px'; } sessionStorage.setItem('__p', JSON.stringify([e.clientX, e.clientY])); }, true);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', crear); else crear(); })();`;

(async () => {
  const browser = await chromium.launch({
    channel: 'msedge', headless: false, ignoreDefaultArgs: ['--enable-automation'],
    args: [`--window-position=${X},${process.env.MONITOR_Y || 0}`, `--window-size=${process.env.ANCHO || 1920},${process.env.ALTO || 1080}`, '--start-maximized',
      '--disable-infobars', '--no-default-browser-check', '--no-first-run', '--disable-features=Translate,TranslateUI'],
  });
  const ctx = await browser.newContext({ viewport: null, locale: 'es-CO' });
  await ctx.addInitScript(CURSOR);
  const page = await ctx.newPage();
  const ir = async (url, ms) => { await page.goto(url); await esperar(ms); };
  const desplazar = async (px, pasos = 15) => { for (let i = 0; i < pasos; i++) { await page.mouse.wheel(0, px / pasos); await esperar(80); } };

  if (modo === 'tienda') {
    await ir(`http://${ip}`, 5000);
    const enlace = page.locator('a[href="/productos"]').first();
    if (await enlace.count()) {
      const b = await enlace.boundingBox();
      await page.mouse.move(b.x + b.width / 2, b.y + b.height / 2, { steps: 40 }); await esperar(600);
      await enlace.click(); await esperar(4000);
    } else await ir(`http://${ip}/productos`, 4000);
    await desplazar(700); await esperar(3000); await desplazar(-700); await esperar(1500);
    await ir(`http://${ip}/api/productos`, 7000);
  } else {
    // El navegador reutiliza la conexion (keep-alive) y siempre responderia el mismo pod:
    // cada peticion se hace desde Node con una conexion nueva, para que se vea el balanceo.
    await page.route(`http://${ip}/**`, (route) => {
      http.get(route.request().url(), { agent: false }, (res) => {
        let cuerpo = ''; res.on('data', (d) => (cuerpo += d));
        res.on('end', () => route.fulfill({ status: res.statusCode, contentType: 'text/html; charset=utf-8',
          // misma respuesta de whoami, en letra grande y marcada para que Edge no ofrezca traducirla
          body: `<html lang="es" translate="no"><meta name="google" content="notranslate"><title>whoami</title>` +
                `<pre style="font:40px/1.35 Consolas,monospace;margin:30px">${cuerpo.replace(/</g, '&lt;')}</pre></html>` }));
      }).on('error', () => route.abort());
    });
    await ir(`http://${ip}`, 3800);
    for (let i = 0; i < 8; i++) { await page.reload(); await esperar(2600); }
  }
  await browser.close();
})();
