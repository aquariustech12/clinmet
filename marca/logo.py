"""Logo ClinMet redibujado en vector (SVG con el texto convertido a trazos, sin depender de fuentes).

Genera:
  clinmet_logo.svg            horizontal: ícono + ClinMet + Clínica Metabólica del Noroeste
  clinmet_logo_blanco.svg     igual, para fondos oscuros
  clinmet_icono.svg           solo el ícono (perfil, favicon)
  clinmet_logo_vertical.svg   ícono arriba, texto abajo (tarjetas, portada)
y PNG transparentes de cada uno con Chromium.
"""
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

AQUI = Path(__file__).parent
FUENTES = Path("/usr/share/fonts/truetype/google-fonts")

TEAL = "#0e8799"
TEAL_OSC = "#03788b"
LIMA = "#a8c62a"
CIAN = "#5bc9e4"
GRIS = "#3e4449"

_fuentes = {}


def fuente(nombre):
    if nombre not in _fuentes:
        _fuentes[nombre] = TTFont(FUENTES / nombre)
    return _fuentes[nombre]


def texto_a_path(texto, archivo, tam, x, y, color, espaciado=0.0):
    """Devuelve (svg <path>, ancho) del texto con la línea base en y."""
    f = fuente(archivo)
    upm = f["head"].unitsPerEm
    gs = f.getGlyphSet()
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    esc = tam / upm
    pen = SVGPathPen(gs)
    cx = 0.0
    for ch in texto:
        g = cmap.get(ord(ch))
        if g is None:
            continue
        tp = TransformPen(pen, (esc, 0, 0, -esc, x + cx, y))
        gs[g].draw(tp)
        cx += hmtx[g][0] * esc + espaciado * tam
    return f'<path fill="{color}" d="{pen.getCommands()}"/>', cx - espaciado * tam


def ancho(texto, archivo, tam, espaciado=0.0):
    return texto_a_path(texto, archivo, tam, 0, 0, "#000", espaciado)[1]


def icono(c_arco=TEAL, c_fig=TEAL, c_lima=LIMA, c_cabeza=TEAL_OSC):
    """Ícono en un cuadro de 200x200: arco abierto, figura con brazos arriba, cinta métrica y hojas."""
    ticks = "".join(
        f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y1 + (7 if i % 2 else 11)}" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round"/>'
        for i, (x, y1) in enumerate([(62 + i * 10.5, 128 + (abs(i - 6) * 0.9)) for i in range(13)])
    )
    return f"""
  <defs>
    <linearGradient id="ga" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0" stop-color="{c_arco}"/><stop offset="1" stop-color="{CIAN}"/>
    </linearGradient>
  </defs>
  <!-- arco abierto -->
  <path d="M150 30 A86 86 0 1 0 172 150" fill="none" stroke="url(#ga)" stroke-width="11" stroke-linecap="round"/>
  <!-- cabeza -->
  <circle cx="104" cy="58" r="17" fill="{c_cabeza}"/>
  <!-- brazo derecho alzado hacia las hojas -->
  <path d="M106 96 C126 82 144 62 156 38 C160 31 168 34 165 42 C152 72 134 96 114 112 Z" fill="{c_fig}"/>
  <!-- brazo izquierdo -->
  <path d="M100 98 C84 88 62 82 40 84 C33 85 33 76 40 75 C66 70 92 76 110 88 Z" fill="{c_fig}" opacity=".9"/>
  <!-- torso y piernas en movimiento -->
  <path d="M96 90 C112 98 120 112 116 132 C112 152 98 168 82 182 C77 186 71 180 76 175 C90 160 98 146 98 132 C98 118 90 108 84 100 Z" fill="{c_fig}"/>
  <path d="M112 132 C126 146 134 162 136 184 C136 191 127 192 126 185 C123 166 116 152 104 142 Z" fill="{c_fig}" opacity=".85"/>
  <!-- cinta métrica alrededor de la cintura -->
  <path d="M50 132 C70 146 132 148 158 120" fill="none" stroke="{c_lima}" stroke-width="14" stroke-linecap="round"/>
  {ticks}
  <path d="M158 120 C166 112 168 104 162 100" fill="none" stroke="{c_lima}" stroke-width="7" stroke-linecap="round"/>
  <!-- hojas -->
  <path d="M164 36 C160 18 170 6 186 2 C190 18 180 32 164 36 Z" fill="{c_lima}"/>
  <path d="M166 40 C176 28 190 28 200 34 C190 46 176 48 166 40 Z" fill="{c_lima}" opacity=".85"/>
"""


def svg_icono(fondo=None):
    bg = f'<rect width="200" height="200" fill="{fondo}"/>' if fondo else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">{bg}{icono()}</svg>'


def svg_horizontal(blanco=False):
    c_clin = "#ffffff" if blanco else GRIS
    c_met = "#7fd8ea" if blanco else TEAL_OSC
    c_sub = "#e6f4f6" if blanco else GRIS
    c_lin = "#7fd8ea" if blanco else TEAL
    w_clin = ancho("Clin", "Poppins-Bold.ttf", 150)
    p_clin, _ = texto_a_path("Clin", "Poppins-Bold.ttf", 150, 250, 150, c_clin)
    p_met, w_met = texto_a_path("Met", "Poppins-Bold.ttf", 150, 250 + w_clin, 150, c_met)
    total = w_clin + w_met
    sub = "Clínica Metabólica del Noroeste"
    tam_sub = 30
    w_sub = ancho(sub, "Poppins-Medium.ttf", tam_sub)
    x_sub = 250 + (total - w_sub) / 2
    p_sub, _ = texto_a_path(sub, "Poppins-Medium.ttf", tam_sub, x_sub, 205, c_sub)
    lineas = (f'<line x1="250" y1="195" x2="{x_sub - 14}" y2="195" stroke="{c_lin}" stroke-width="3"/>'
              f'<line x1="{x_sub + w_sub + 14}" y1="195" x2="{250 + total}" y2="195" stroke="{c_lin}" stroke-width="3"/>')
    W = 250 + total + 20
    sep = f'<line x1="228" y1="40" x2="228" y2="200" stroke="{c_lin}" stroke-width="3"/>'
    ic = icono(c_arco="#7fd8ea" if blanco else TEAL, c_fig="#ffffff" if blanco else TEAL,
               c_cabeza="#ffffff" if blanco else TEAL_OSC)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} 230">'
            f'<g transform="translate(5,15)">{ic}</g>{sep}{p_clin}{p_met}{p_sub}{lineas}</svg>')


def svg_vertical(blanco=False):
    c_clin = "#ffffff" if blanco else GRIS
    c_met = "#7fd8ea" if blanco else TEAL_OSC
    c_sub = "#e6f4f6" if blanco else GRIS
    w_clin = ancho("Clin", "Poppins-Bold.ttf", 120)
    w_met = ancho("Met", "Poppins-Bold.ttf", 120)
    total = w_clin + w_met
    sub = "Clínica Metabólica del Noroeste"
    w_sub = ancho(sub, "Poppins-Medium.ttf", 26)
    W = max(total, w_sub) + 40
    x0 = (W - total) / 2
    p_clin, _ = texto_a_path("Clin", "Poppins-Bold.ttf", 120, x0, 330, c_clin)
    p_met, _ = texto_a_path("Met", "Poppins-Bold.ttf", 120, x0 + w_clin, 330, c_met)
    p_sub, _ = texto_a_path(sub, "Poppins-Medium.ttf", 26, (W - w_sub) / 2, 380, c_sub)
    ic = icono(c_arco="#7fd8ea" if blanco else TEAL, c_fig="#ffffff" if blanco else TEAL,
               c_cabeza="#ffffff" if blanco else TEAL_OSC)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} 400">'
            f'<g transform="translate({(W - 200) / 2:.1f},0)">{ic}</g>{p_clin}{p_met}{p_sub}</svg>')


PIEZAS = {
    "clinmet_logo": (svg_horizontal, {}),
    "clinmet_logo_blanco": (svg_horizontal, {"blanco": True}),
    "clinmet_logo_vertical": (svg_vertical, {}),
    "clinmet_icono": (svg_icono, {}),
}


def main():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        for nombre, (fn, kw) in PIEZAS.items():
            svg = fn(**kw)
            (AQUI / f"{nombre}.svg").write_text(svg)
            vb = [float(v) for v in svg.split('viewBox="')[1].split('"')[0].split()]
            esc = 2000 / vb[2] if vb[2] > vb[3] else 1200 / vb[3]
            w, h = int(vb[2] * esc), int(vb[3] * esc)
            pg = b.new_page(viewport={"width": w, "height": h})
            inline = svg.replace("<svg ", f'<svg width="{w}" height="{h}" ', 1)
            pg.set_content(f'<html><body style="margin:0;background:transparent">{inline}</body></html>')
            pg.screenshot(path=str(AQUI / f"{nombre}.png"), omit_background=True)
            pg.close()
        b.close()
    print("ok")


if __name__ == "__main__":
    main()
