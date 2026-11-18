"""Construye la presentación completa como un único HTML autónomo.

Lee las diapositivas de la presentación de claude.ai y las junta en un HTML con
visor propio (flechas, notas del orador, PDF, huecos editables). Las imágenes se
incrustan en el HTML, así que el resultado es un solo fichero.

Carpeta fuente: la de la presentación, con esta forma (se obtiene al leer los
ficheros de la presentación en claude.ai):

    project/deck.json          orden de las diapositivas y título
    project/deck.css           estilos compartidos
    project/slides/<id>.html   una diapositiva por fichero

Las imágenes de las diapositivas aparecen como /_blob/<id>; cada una se asocia
a un fichero local con --imagen <id>=<ruta>.

Uso:
    python docs/presentaciones/construir_presentacion.py CARPETA_FUENTE SALIDA.html \\
        --imagen <id>=docs/img/a_ausentes.png --imagen <id>=docs/img/c_vigor.png
"""

import argparse
import base64
import json
import sys
from pathlib import Path

ESTILOS_VISOR = """
* { margin: 0; }
p, li, h1, h2, h3, td, th { overflow-wrap: break-word; }
table { border-collapse: separate; border-spacing: 0; border: solid #0003; border-width: 2px 0 0 2px; }
th, td { padding: .35em .6em; text-align: left; border: solid #0003; border-width: 0 2px 2px 0; }
html, body { margin: 0; height: 100%; background: #0B1A15; overflow: hidden; }
#stage { position: fixed; inset: 0 0 56px 0; overflow: hidden; }
#deck { position: absolute; left: 50%; top: 50%; width: 1920px; height: 1080px; transform-origin: center center; }
#deck > section { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; box-sizing: border-box; overflow: hidden; display: none; }
#deck > section.active { display: block; }
#deck > section::after { content: attr(data-n); }
#deck > section.cover::before, #deck > section.cover::after { content: none; }
aside { display: none; }
x-shape, x-icon { display: block; }
x-shape[kind="arrow-right"] { clip-path: polygon(0 28%, 58% 28%, 58% 0, 100% 50%, 58% 100%, 58% 72%, 0 72%); }
.shotbox { cursor: pointer; }
.shotbox:hover { border-color: #1F7A58; }
.ph[contenteditable="true"] { outline: none; cursor: text; }
.ph[contenteditable="true"]:hover, .ph[contenteditable="true"]:focus { background: #CFE6DA; border-radius: 6px; }
#bar { position: fixed; left: 0; right: 0; bottom: 0; height: 56px; display: flex; align-items: center; justify-content: center; gap: 10px; background: #10241E; color: #E9EFE9; font: 600 16px/1 Inter, Arial, sans-serif; z-index: 10; }
#bar button { font: inherit; color: #E9EFE9; background: #1B3A30; border: 1px solid #2F5A4A; border-radius: 8px; padding: 9px 14px; cursor: pointer; }
#bar button:hover { background: #24503F; }
#bar button.on { background: #1F7A58; }
#bar .sep { width: 1px; height: 24px; background: #2F5A4A; margin: 0 6px; }
#pos { min-width: 70px; text-align: center; }
#notes { position: fixed; left: 0; right: 0; bottom: 56px; max-height: 28vh; overflow: auto; padding: 14px 24px; background: rgba(16, 36, 30, .96); color: #E9EFE9; font: 400 20px/1.4 Inter, Arial, sans-serif; display: none; z-index: 9; }
#notes.show { display: block; }
@media print {
  html, body { height: auto; overflow: visible; background: none; }
  #stage { position: static; overflow: visible; }
  #deck { position: static; transform: none !important; width: auto; height: auto; }
  #deck > section { display: block !important; position: relative; break-after: page; page-break-after: always; }
  #bar, #notes { display: none !important; }
  .anim { animation: none !important; }
  @page { size: 1920px 1080px; margin: 0; }
}
"""

SCRIPT_VISOR = r"""
(function () {
  var deck = document.getElementById('deck');
  var slides = Array.prototype.slice.call(deck.children).filter(function (n) { return n.tagName === 'SECTION'; });
  var pos = document.getElementById('pos');
  var notes = document.getElementById('notes');
  var cur = 0;

  slides.forEach(function (s, i) { s.setAttribute('data-n', i + 1); });

  var GEAR = 'M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58a.49.49 0 0 0 .12-.61l-1.92-3.32a.488.488 0 0 0-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54a.484.484 0 0 0-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58a.49.49 0 0 0-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z';
  Array.prototype.forEach.call(deck.querySelectorAll('x-icon[name="Settings"]'), function (el) {
    if (!el.querySelector('svg')) {
      el.innerHTML = '<svg viewBox="0 0 24 24" width="100%" height="100%" fill="currentColor"><path d="' + GEAR + '"/></svg>';
    }
  });
  Array.prototype.forEach.call(deck.querySelectorAll('a[href^="http"]'), function (a) { a.target = '_blank'; a.rel = 'noopener'; });

  function show(i) {
    cur = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach(function (s, k) { s.classList.toggle('active', k === cur); });
    pos.textContent = (cur + 1) + ' / ' + slides.length;
    var a = slides[cur].querySelector('aside');
    notes.textContent = a ? a.textContent : '';
    try { history.replaceState(null, '', '#' + (cur + 1)); } catch (e) {}
  }
  function fit() {
    var s = Math.min(window.innerWidth / 1920, (window.innerHeight - 56) / 1080);
    deck.style.transform = 'translate(-50%, -50%) scale(' + s + ')';
  }

  // Placeholders de texto
  Array.prototype.forEach.call(deck.querySelectorAll('.ph'), function (el) {
    el.setAttribute('contenteditable', 'true');
    el.addEventListener('focus', function () {
      if (el.classList.contains('ph')) {
        var r = document.createRange(); r.selectNodeContents(el);
        var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
      }
    });
    el.addEventListener('input', function () { el.classList.remove('ph'); });
  });

  // Placeholders de captura: clic, arrastrar o pegar
  var picker = document.createElement('input');
  picker.type = 'file'; picker.accept = 'image/*'; picker.style.display = 'none';
  document.body.appendChild(picker);
  var pickTarget = null, hoverBox = null;
  function setImage(box, file) {
    var reader = new FileReader();
    reader.onload = function () {
      box.innerHTML = '';
      var img = new Image();
      img.src = reader.result; img.alt = 'Captura';
      img.style.cssText = 'max-width:100%;max-height:100%;object-fit:contain;border-radius:12px';
      box.appendChild(img);
      box.style.padding = '0'; box.style.borderStyle = 'solid'; box.style.borderColor = 'transparent';
    };
    reader.readAsDataURL(file);
  }
  Array.prototype.forEach.call(deck.querySelectorAll('.shotbox'), function (box) {
    box.tabIndex = 0;
    box.title = 'Haz clic, arrastra una imagen o pega una captura (Ctrl+V)';
    box.addEventListener('mouseenter', function () { hoverBox = box; });
    box.addEventListener('mouseleave', function () { if (hoverBox === box) hoverBox = null; });
    box.addEventListener('dragover', function (e) { e.preventDefault(); });
    box.addEventListener('drop', function (e) {
      e.preventDefault();
      var f = e.dataTransfer.files[0];
      if (f && f.type.indexOf('image') === 0) setImage(box, f);
    });
    box.addEventListener('click', function () { pickTarget = box; picker.value = ''; picker.click(); });
  });
  picker.addEventListener('change', function () {
    if (picker.files[0] && pickTarget) setImage(pickTarget, picker.files[0]);
  });
  document.addEventListener('paste', function (e) {
    var ae = document.activeElement;
    var box = (ae && ae.closest && ae.closest('.shotbox')) || hoverBox;
    if (!box || !e.clipboardData) return;
    for (var i = 0; i < e.clipboardData.items.length; i++) {
      var it = e.clipboardData.items[i];
      if (it.type.indexOf('image') === 0) { setImage(box, it.getAsFile()); e.preventDefault(); break; }
    }
  });

  // Navegación
  document.getElementById('prev').onclick = function () { show(cur - 1); };
  document.getElementById('next').onclick = function () { show(cur + 1); };
  document.addEventListener('keydown', function (e) {
    if (e.target && (e.target.isContentEditable || e.target.tagName === 'INPUT')) return;
    var k = e.key;
    if (k === 'ArrowRight' || k === 'PageDown' || k === ' ') { show(cur + 1); e.preventDefault(); }
    else if (k === 'ArrowLeft' || k === 'PageUp') { show(cur - 1); e.preventDefault(); }
    else if (k === 'Home') { show(0); }
    else if (k === 'End') { show(slides.length - 1); }
    else if (k === 'n' || k === 'N') { notes.classList.toggle('show'); }
  });
  window.addEventListener('resize', fit);
  window.addEventListener('hashchange', function () { var n = parseInt(location.hash.slice(1), 10); if (n) show(n - 1); });

  // Barra
  document.getElementById('btn-notes').onclick = function () { notes.classList.toggle('show'); this.classList.toggle('on'); };
  document.getElementById('btn-edit').onclick = function () {
    var on = deck.getAttribute('contenteditable') !== 'true';
    deck.setAttribute('contenteditable', on ? 'true' : 'false');
    this.classList.toggle('on', on);
  };
  document.getElementById('btn-print').onclick = function () { window.print(); };
  document.getElementById('btn-save').onclick = function () {
    var wasOn = deck.getAttribute('contenteditable') === 'true';
    deck.setAttribute('contenteditable', 'false');
    var clone = document.documentElement.cloneNode(true);
    var d = clone.querySelector('#deck'); d.removeAttribute('contenteditable');
    var inputs = clone.querySelectorAll('input[type=file]'); Array.prototype.forEach.call(inputs, function (n) { n.remove(); });
    var html = '<!doctype html>\n' + clone.outerHTML;
    var a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([html], { type: 'text/html' }));
    a.download = 'presentacion-eucalyptus.html';
    document.body.appendChild(a); a.click(); a.remove();
    if (wasOn) deck.setAttribute('contenteditable', 'true');
  };

  fit();
  var start = parseInt(location.hash.slice(1), 10);
  show(start ? start - 1 : 0);
})();
"""

PLANTILLA_PAGINA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<!-- Presentación autónoma. Flechas o espacio para moverse, N para las notas del orador.
     Rellenar los recuadros: clic en el texto entre corchetes para escribir; clic, arrastrar o pegar (Ctrl+V)
     una imagen en los recuadros de captura. «Guardar mi versión» descarga este mismo fichero con los cambios. -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400..700&family=Inter:wght@400;600&display=swap">
<style>
{css}
{estilos_visor}
</style>
</head>
<body>
<div id="stage"><div id="deck">
{cuerpo}
</div></div>
<div id="notes"></div>
<div id="bar">
  <button id="prev" title="Anterior (←)">◀</button><span id="pos">1</span><button id="next" title="Siguiente (→)">▶</button>
  <span class="sep"></span>
  <button id="btn-notes" title="Notas del orador (N)">Notas</button>
  <button id="btn-edit" title="Editar cualquier texto de las diapositivas">Editar texto</button>
  <button id="btn-save" title="Descarga este HTML con tus cambios">Guardar mi versión</button>
  <button id="btn-print" title="Imprimir o guardar como PDF">PDF</button>
</div>
<script>
{script_visor}
</script>
</body>
</html>
"""


def leer_argumentos():
    analizador = argparse.ArgumentParser(description="Construye la presentación completa en un único HTML.")
    analizador.add_argument("fuente", type=Path, help="carpeta con project/deck.json, deck.css y slides/")
    analizador.add_argument("salida", type=Path, help="fichero HTML que se genera")
    analizador.add_argument(
        "--imagen",
        action="append",
        default=[],
        metavar="ID=RUTA",
        help="asocia un /_blob/<id> de las diapositivas a un fichero de imagen (se puede repetir)",
    )
    return analizador.parse_args()


def leer_imagenes(asociaciones):
    """Devuelve {id: ruta} a partir de los argumentos --imagen ID=RUTA."""
    imagenes = {}
    for asociacion in asociaciones:
        identificador, separador, ruta = asociacion.partition("=")
        if not separador or not ruta:
            raise SystemExit(f"--imagen espera ID=RUTA, no «{asociacion}»")
        imagenes[identificador] = Path(ruta)
    return imagenes


def leer_diapositivas(fuente, orden):
    carpeta = fuente / "project" / "slides"
    return [(carpeta / f"{identificador}.html").read_text(encoding="utf-8").strip() for identificador in orden]


def incrustar_imagenes(cuerpo, imagenes):
    for identificador, ruta in imagenes.items():
        datos = base64.b64encode(ruta.read_bytes()).decode("ascii")
        cuerpo = cuerpo.replace(f"/_blob/{identificador}", f"data:image/png;base64,{datos}")
    if "/_blob/" in cuerpo:
        raise SystemExit("Queda una imagen sin incrustar: falta alguna opción --imagen")
    return cuerpo


def componer_pagina(titulo, css, cuerpo):
    return PLANTILLA_PAGINA.format(
        titulo=titulo,
        css=css,
        estilos_visor=ESTILOS_VISOR,
        cuerpo=cuerpo,
        script_visor=SCRIPT_VISOR,
    )


def main():
    argumentos = leer_argumentos()
    presentacion = json.loads((argumentos.fuente / "project" / "deck.json").read_text(encoding="utf-8"))
    css = (argumentos.fuente / "project" / "deck.css").read_text(encoding="utf-8")

    diapositivas = leer_diapositivas(argumentos.fuente, presentacion["order"])
    cuerpo = incrustar_imagenes("\n".join(diapositivas), leer_imagenes(argumentos.imagen))

    argumentos.salida.parent.mkdir(parents=True, exist_ok=True)
    argumentos.salida.write_text(componer_pagina(presentacion["title"], css, cuerpo), encoding="utf-8", newline="\n")
    print(f"{len(diapositivas)} diapositivas, {argumentos.salida.stat().st_size // 1024} KB -> {argumentos.salida}")


if __name__ == "__main__":
    sys.exit(main())
