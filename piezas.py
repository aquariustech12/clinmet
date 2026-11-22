"""Piezas de ClinMet: banner roll-up 80x200 cm, tarjetas 9x5 cm, publicaciones y anuncios 1080 px.

Línea legal en todo: "Consultorio médico del Dr. Luis Alejandro López Valenzuela…" + datos de César,
leyenda "Cada paciente requiere valoración médica. Los resultados varían." y el aviso de publicidad.
Sin nombres de medicamentos ni promesas de resultados.
Uso: python3 piezas.py   (deja todo en piezas/)
"""
import base64
from pathlib import Path

import segno
from playwright.sync_api import sync_playwright

AQUI = Path(__file__).parent
OUT = AQUI / "piezas"
MARCA = AQUI / "marca"
FOTOS = AQUI / "fotos"
FUENTES = Path("/usr/share/fonts/truetype/google-fonts")

TEAL, TEAL_OSC, LIMA, CIAN, GRIS, FONDO = "#0e8799", "#03788b", "#a8c62a", "#5bc9e4", "#3e4449", "#f5fafb"

WA = "526441898923"
WA_VISIBLE = "644 189 8923"
QR_TEXTO = "Hola, quiero informes del programa de control de peso"   # el agente lo cuenta como canal "QR"
AVISO_PUB = "2626042002A00077"
LEYENDA = "Cada paciente requiere valoración médica. Los resultados varían."
DOCTOR = ("Consultorio médico del Dr. Luis Alejandro López Valenzuela · Médico general · Universidad Santander · "
          "Cédula profesional 14747768 · Diplomado en Bariatría clínica")
NUTRI = "Ln. César Alfredo Romero Palafox · Nutriólogo · Universidad La Salle Noroeste · Cédula profesional 11230740"
DIRECCION = "Consultorio 7, Clínica Santa Elena · Av. Guerrero 826, entre California y Quintana Roo, Col. Del Valle, Cd. Obregón, Son."
HORARIO = "Lunes a sábado · 8:00 a 13:00 y 15:00 a 20:30"


def b64(p: Path, mime: str) -> str:
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


def svg_inline(nombre: str, ancho: str) -> str:
    s = (MARCA / f"{nombre}.svg").read_text()
    return f'<div style="width:{ancho};flex:none">' + s.replace("<svg ", '<svg style="width:100%;height:auto;display:block" ', 1) + "</div>"


QR_LAB = "Hola, vi su anuncio en el laboratorio y quiero informes"   # canal "Banner laboratorio" en el agente


def qr_svg(texto: str = QR_TEXTO) -> str:
    q = segno.make(f"https://wa.me/{WA}?text={texto.replace(' ', '%20')}", error="m")
    import io
    buf = io.BytesIO()
    q.save(buf, kind="svg", scale=10, border=2, dark=TEAL_OSC, light="#ffffff", xmldecl=False, svgns=True)
    s = buf.getvalue().decode()
    # segno no pone viewBox: sin él, al escalar el SVG se recorta el QR y deja de leerse
    import re
    w, h = re.search(r'width="(\d+)" height="(\d+)"', s).groups()
    s = s.replace("<svg ", f'<svg viewBox="0 0 {w} {h}" style="width:100%;height:auto;display:block" ', 1)
    return s


CSS = f"""
@font-face{{font-family:P;src:url('{(FUENTES / "Poppins-Regular.ttf").as_uri()}');font-weight:400}}
@font-face{{font-family:P;src:url('{(FUENTES / "Poppins-Medium.ttf").as_uri()}');font-weight:500}}
@font-face{{font-family:P;src:url('{(FUENTES / "Poppins-Bold.ttf").as_uri()}');font-weight:700}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:P,sans-serif;color:{GRIS};background:{FONDO}}}
.t{{color:{TEAL_OSC}}} .l{{color:{LIMA}}}
"""


def pagina(cuerpo: str, w: str, h: str, extra: str = "") -> str:
    return f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}@page{{size:{w} {h};margin:0}}body{{width:{w};height:{h};overflow:hidden}}{extra}</style></head><body>{cuerpo}</body></html>"


# ---------------- banner roll-up 80 x 200 cm (diseñado a 800 x 2000 px, se escala) ----------------
def banner(kicker="CIUDAD OBREGÓN", titulo='Programa <span class=t>médico</span> de control de peso',
           sub="Te valora un médico en persona, con estudios de laboratorio y un plan con nutriólogo.",
           qr_texto=QR_TEXTO, cta="Agenda tu valoración", extra_bloque="") -> str:
    puntos = [("Valoración médica presencial", "M12 2v6a4 4 0 0 0 8 0V2M16 12v3a5 5 0 0 1-10 0v-1"),
              ("Estudios de laboratorio", "M9 2v6L4 18a2 2 0 0 0 2 3h12a2 2 0 0 0 2-3L15 8V2M8 2h8"),
              ("Plan con nutriólogo", "M12 7c-3-4-9-2-8 4 1 5 5 10 8 10s7-5 8-10c1-6-5-8-8-4zM12 7c0-2 1-4 3-5")]
    lista = "".join(f'''<div class=p><span class=i><svg viewBox="0 0 24 24" fill="none" stroke="{TEAL_OSC}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="{d}"/></svg></span>{t}</div>''' for t, d in puntos)
    extra = f"""
.w{{width:800px;height:2000px;padding:70px 60px 50px;display:flex;flex-direction:column;border-top:18px solid {TEAL}}}
.k{{font-weight:700;letter-spacing:.12em;color:{TEAL};font-size:26px;margin-top:36px}}
h1{{font-weight:700;font-size:78px;line-height:1.02;color:{GRIS};margin-top:12px}}
.s{{font-size:30px;line-height:1.38;margin-top:22px}}
.p{{display:flex;align-items:center;gap:26px;font-weight:700;font-size:32px;margin-top:22px}}
.i{{width:72px;height:72px;border-radius:50%;background:#dff2f4;display:flex;align-items:center;justify-content:center;flex:none}}.i svg{{width:38px}}
.n{{font-size:24px;line-height:1.4;margin-top:26px}}
.cta{{margin-top:auto;background:{TEAL_OSC};border-radius:22px;padding:30px 40px;text-align:center;color:#fff}}
.cta h2{{font-size:50px}}.q{{width:270px;margin:18px auto 14px;background:#fff;border-radius:16px;padding:14px}}
.cta .e{{color:#c9eef3;font-size:26px}}.cta .num{{font-weight:700;font-size:56px;letter-spacing:.02em}}
.leg{{margin-top:26px;font-size:16px;line-height:1.5}}.leg b{{font-size:19px}}
.gym{{margin-top:18px;background:#eef6d6;border-left:8px solid {LIMA};padding:14px 20px;font-size:24px;line-height:1.35;border-radius:0 14px 14px 0}}
"""
    cuerpo = f"""<div class=w>{svg_inline("clinmet_logo", "640px")}
<div class=k>{kicker}</div>
<h1>{titulo}</h1>
<div class=s>{sub}</div>
{extra_bloque}{lista}
<div class=n>Si un tratamiento con medicamento está indicado para ti, lo decide el médico en tu consulta.</div>
<div class=cta><h2>{cta}</h2><div class=q>{qr_svg(qr_texto)}</div>
<div class=e>Escanea o escribe por WhatsApp</div><div class=num>{WA_VISIBLE}</div></div>
<div class=leg><b><i>{LEYENDA}</i></b><br>{DOCTOR}<br>{NUTRI}<br>{DIRECCION}<br>Aviso de publicidad COFEPRIS {AVISO_PUB}</div></div>"""
    return pagina(cuerpo, "800px", "2000px", extra)


# ---------------- banner de laboratorio con el layout de César (80 x 200 cm) ----------------
def _ico(d: str, color: str = None, w: str = "2") -> str:
    return (f'<svg viewBox="0 0 48 48" fill="none" stroke="{color or TEAL_OSC}" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round">{d}</svg>')


ICONOS = {
    "glucosa": '<path d="M20 6c6 8 11 14 11 20a11 11 0 0 1-22 0c0-6 5-12 11-20z"/><rect x="26" y="28" width="12" height="12" rx="1.5"/><path d="M26 32l6-3 6 3M32 29v11"/>',
    "colesterol": '<path d="M24 6c7 9 12 16 12 22a12 12 0 0 1-24 0c0-6 5-13 12-22z"/><path d="M18 30a6 6 0 0 0 6 6"/>',
    "trigliceridos": '<path d="M17 8c5 7 9 12 9 17a9 9 0 0 1-18 0c0-5 4-10 9-17z"/><path d="M33 16c3 5 6 8 6 11a6 6 0 0 1-12 0c0-3 3-6 6-11zM34 33c2 3 4 5 4 7a4 4 0 0 1-8 0c0-2 2-4 4-7z"/>',
    "insulina": '<path d="M12 10c3 4 6 8 6 11a6 6 0 0 1-12 0c0-3 3-7 6-11z"/><rect x="24" y="8" width="16" height="30" rx="4"/><rect x="28" y="13" width="8" height="9" rx="1"/><path d="M32 38v4"/>',
    "peso": '<path d="M16 8c0 6-2 10-2 16s4 10 10 10 10-4 10-10-2-10-2-16"/><path d="M18 40c2 2 4 3 6 3s4-1 6-3"/><path d="M4 22h8m-3-3 3 3-3 3M44 22h-8m3-3-3 3 3 3"/>',
    "medico": '<path d="M14 6v10a8 8 0 0 0 16 0V6"/><path d="M22 24v6a8 8 0 0 0 16 0v-4"/><circle cx="38" cy="22" r="4"/>',
    "lab": '<path d="M18 6v12L8 38a3 3 0 0 0 3 4h26a3 3 0 0 0 3-4L30 18V6M16 6h16"/><path d="M13 30h22"/><circle cx="22" cy="35" r="1.5"/><circle cx="28" cy="33" r="1"/>',
    "manzana": '<path d="M24 14c-5-5-15-3-15 8 0 9 7 20 15 20s15-11 15-20c0-11-10-13-15-8z"/><path d="M24 14c0-4 2-7 6-8M26 10c4-3 8-2 10 0-3 2-7 2-10 0z"/>',
    "check": '<path d="M14 24l7 7 13-14"/>',
    "cal": '<rect x="6" y="10" width="36" height="32" rx="4"/><path d="M6 18h36M16 6v8M32 6v8M13 25h5v5h-5zM22 25h5v5h-5zM31 25h5v5h-5zM13 33h5v5h-5zM22 33h5v5h-5z"/>',
    "wa": '<path d="M24 6a17 17 0 0 0-14.7 25.6L7 41l9.7-2.3A17 17 0 1 0 24 6z"/><path d="M17.5 16.5c-.6 1.5.2 4.4 2.6 7.3 2.6 3 5.6 4.6 7.4 4.2 1-.2 2-1.3 2.2-2.2l-3-1.6-1.6 1.3c-1.6-.6-3.6-2.5-4.3-4.1l1.3-1.6-1.5-3.1c-1 .1-2.6 1-3.1 1.8z"/>',
    "pin": '<path d="M24 44s14-12 14-24a14 14 0 0 0-28 0c0 12 14 24 14 24z"/><circle cx="24" cy="20" r="5"/>',
}


def banner_metabolico(qr_texto: str = QR_LAB) -> str:
    cond = [("glucosa", "Glucosa<br>alta"), ("colesterol", "Colesterol<br>elevado"), ("trigliceridos", "Triglicéridos<br>altos"),
            ("insulina", "Resistencia<br>a la insulina"), ("peso", "Dificultad para<br>bajar de peso")]
    celdas = "".join(f'<div class=cd><div class=ci>{_ico(ICONOS[k])}</div><div class=ct>{t}</div></div>' for k, t in cond)
    serv = [("medico", "Valoración<br>médica presencial"), ("lab", "Estudios<br>de laboratorio"), ("manzana", "Plan personalizado<br>con nutriólogo")]
    servicios = "".join(f'<div class=sv><div class=si>{_ico(ICONOS[k], "#ffffff", "2.4")}</div><div class=st>{t}</div></div>' for k, t in serv)
    hexes = "".join(f'<polygon points="{x+20},{y} {x+40},{y+11} {x+40},{y+34} {x+20},{y+45} {x},{y+34} {x},{y+11}"/>'
                    for x, y in [(0, 0), (44, 25), (0, 50), (88, 0), (44, 75), (88, 50)])
    deco = f'<svg class=hx viewBox="0 0 130 125" fill="none" stroke="{CIAN}" stroke-width="1.4" opacity=".35">{hexes}</svg>'
    extra = f"""
body{{background:#fff}}
.w{{width:800px;height:2000px;position:relative;overflow:hidden;display:flex;flex-direction:column;align-items:center;
   background:linear-gradient(180deg,#f3fbfc 0%,#ffffff 30%,#f3fbfc 100%)}}
.hx{{position:absolute;width:190px;top:24px}} .hx.l{{left:-30px}} .hx.r{{right:-30px;transform:scaleX(-1)}}
.ola{{position:absolute;left:0;width:800px}}
.logo{{margin-top:40px;position:relative}}
h1{{font-weight:700;font-size:54px;line-height:1.08;text-align:center;color:{GRIS};margin-top:22px;position:relative}}
h1 b{{display:block;font-size:72px;color:{TEAL_OSC};white-space:nowrap}}
.sub{{font-size:31px;margin-top:14px;text-align:center}}
.sub:after{{content:"";display:block;width:260px;height:6px;border-radius:3px;background:{LIMA};margin:12px auto 0}}
.cds{{display:flex;flex-wrap:wrap;justify-content:center;gap:18px 22px;width:720px;margin-top:20px}}
.cd{{width:212px;text-align:center}}
.ci{{width:104px;height:104px;margin:0 auto;border-radius:50%;background:#e3f4f6;display:flex;align-items:center;justify-content:center}}
.ci svg{{width:58px}}
.ct{{font-weight:500;font-size:24px;line-height:1.18;margin-top:8px}}
.pill{{margin-top:20px;width:720px;background:#dff2f4;border-radius:40px;padding:14px 24px;font-weight:700;font-size:27px;color:{GRIS};text-align:center}}
.band{{margin-top:20px;width:720px;background:linear-gradient(135deg,{TEAL_OSC},#055f6e);border-radius:34px;padding:24px 30px 22px;text-align:center;color:#fff}}
.band .m{{font-weight:700;font-size:58px;line-height:1}} .band .m span{{color:{LIMA}}}
.band .e{{font-style:italic;font-size:32px;margin-top:10px;color:#d9f1f4}}
.svs{{display:flex;justify-content:space-between;width:690px;margin-top:18px}}
.sv{{width:220px;text-align:center}}
.si{{width:96px;height:96px;margin:0 auto;border-radius:50%;background:{TEAL};display:flex;align-items:center;justify-content:center}}.si svg{{width:52px}}
.st{{font-weight:700;font-size:23px;line-height:1.18;margin-top:8px;color:{GRIS}}}
.nota{{margin-top:18px;width:720px;display:flex;gap:18px;align-items:center;background:#eef7f8;border-radius:24px;padding:14px 22px;font-size:22px;line-height:1.3}}
.nota .ck{{width:56px;height:56px;border-radius:50%;background:{LIMA};flex:none;display:flex;align-items:center;justify-content:center}}.ck svg{{width:34px}}
.cta{{margin-top:20px;width:720px;background:{TEAL_OSC};border-radius:30px;padding:22px 24px;display:flex;align-items:center;gap:26px;color:#fff}}
.cta .ag{{flex:1}}
.cta .bt{{display:flex;align-items:center;gap:16px;background:{LIMA};color:{GRIS};border-radius:22px;padding:14px 18px;font-weight:700;font-size:34px;line-height:1.05}}
.cta .bt svg{{width:62px;flex:none}}
.cta .es{{font-size:22px;color:#cdeff3;margin-top:18px}}
.cta .nm{{display:flex;align-items:center;gap:12px;font-weight:700;font-size:44px;margin-top:4px}}.cta .nm svg{{width:44px}}
.cta .q{{width:220px;background:#fff;border-radius:18px;padding:10px;flex:none}}
.tag{{margin-top:16px;font-weight:700;font-style:italic;font-size:28px;color:{TEAL_OSC};text-align:center}}
.pie{{margin-top:auto;width:800px;background:linear-gradient(180deg,{TEAL_OSC},#04505c);color:#e8f6f8;padding:18px 40px 22px;text-align:center;font-size:16px;line-height:1.5}}
.pie b{{color:#fff}} .pie .ley{{font-weight:700;font-size:19px;color:#fff;margin-bottom:6px}}
.pie .dir{{display:flex;justify-content:center;align-items:center;gap:10px;margin-top:10px;font-size:17px}}.pie .dir svg{{width:26px;flex:none}}
.pie .av{{display:inline-block;margin-top:10px;border:1.5px solid #9fdbe4;border-radius:30px;padding:8px 24px;font-size:18px}}
"""
    cuerpo = f"""<div class=w>{deco.replace('class=hx', 'class="hx l"')}{deco.replace('class=hx', 'class="hx r"')}
<div class=logo>{svg_inline("clinmet_logo", "540px")}</div>
<h1>¿Cómo está tu<b>salud metabólica?</b></h1>
<div class=sub>Puede que no solo se trate de tu peso…</div>
<div class=cds>{celdas}</div>
<div class=pill>Conoce tus números y entiende qué necesitas.</div>
<div class=band><div class=m>Médico <span>+</span> Nutriólogo</div><div class=e>Una evaluación integral para ti</div></div>
<div class=svs>{servicios}</div>
<div class=nota><div class=ck>{_ico(ICONOS["check"], "#ffffff", "4")}</div><div>Si un tratamiento con medicamento está indicado para ti, <b>lo decide el médico</b> en tu consulta.</div></div>
<div class=cta><div class=ag><div class=bt>{_ico(ICONOS["cal"], GRIS, "2.6")}Agenda tu valoración</div>
<div class=es>Escanea o escribe por WhatsApp</div><div class=nm>{_ico(ICONOS["wa"], "#ffffff", "2.4")}{WA_VISIBLE}</div></div>
<div class=q>{qr_svg(qr_texto)}</div></div>
<div class=tag>Cuida tu salud hoy, mejora tu calidad de vida.</div>
<div class=pie><div class=ley>{LEYENDA}</div>{DOCTOR}<br>{NUTRI}
<div class=dir>{_ico(ICONOS["pin"], "#ffffff", "2.6")}<span>{DIRECCION}</span></div>
<div class=av>Aviso de publicidad <b>COFEPRIS {AVISO_PUB}</b></div></div></div>"""
    return pagina(cuerpo, "800px", "2000px", extra)


# ---------------- tarjetas 9 x 5 cm (frente común + reverso por persona) ----------------
def tarjeta_frente() -> str:
    extra = f".w{{width:90mm;height:50mm;background:#fff;display:flex;align-items:center;justify-content:center;border-bottom:3mm solid {TEAL}}}"
    return pagina(f'<div class=w>{svg_inline("clinmet_logo", "72mm")}</div>', "90mm", "50mm", extra)


def tarjeta_reverso(nombre: str, cargo: str, linea_legal: str) -> str:
    extra = f"""
.w{{width:90mm;height:50mm;background:#fff;padding:5mm 6mm 4mm;display:flex;flex-direction:column;border-left:2.5mm solid {LIMA}}}
.top{{display:flex;justify-content:space-between;align-items:flex-start}}
.n{{font-weight:700;font-size:11.5pt;line-height:1.15;color:{GRIS}}}.c{{font-size:8pt;color:{TEAL_OSC};font-weight:500;margin-top:1mm}}
.ic{{width:11mm}}
.d{{font-size:7.4pt;line-height:1.5;margin-top:auto}}.d b{{color:{TEAL_OSC}}}
.lg{{font-size:5.6pt;line-height:1.35;margin-top:1.6mm;color:#6a7278}}"""
    cuerpo = f"""<div class=w><div class=top><div><div class=n>{nombre}</div><div class=c>{cargo}</div></div>{svg_inline("clinmet_icono", "11mm")}</div>
<div class=d><b>WhatsApp</b> {WA_VISIBLE}<br>Consultorio 7, Clínica Santa Elena · Av. Guerrero 826, Col. Del Valle, Cd. Obregón<br>{HORARIO}</div>
<div class=lg>{linea_legal} · {LEYENDA} · Aviso de publicidad COFEPRIS {AVISO_PUB}</div></div>"""
    return pagina(cuerpo, "90mm", "50mm", extra)


# ---------------- publicaciones 1080 x 1350 ----------------
def post(titulo: str, texto: str, foto: str | None = None, recorte: str = "center 30%", kicker: str = "") -> str:
    foto_html = (f'<div class=f style="background-image:url({b64(FOTOS / foto, "image/png")});background-position:{recorte}"></div>'
                 if foto else "")
    extra = f"""
.w{{width:1080px;height:1350px;display:flex;flex-direction:column;background:{FONDO}}}
.h{{padding:46px 64px 0;display:flex;justify-content:space-between;align-items:center}}
.f{{flex:1;margin:34px 64px 0;border-radius:28px;background-size:cover}}
.b{{padding:{"38px" if foto else "0"} 64px 0;{"" if foto else "flex:1;display:flex;flex-direction:column;justify-content:center;position:relative"}}}
.wm{{position:absolute;right:40px;bottom:10px;width:380px;opacity:.12}}
.k{{font-weight:700;letter-spacing:.12em;color:{TEAL};font-size:24px}}
h1{{font-weight:700;font-size:{60 if foto else 82}px;line-height:1.08;margin-top:10px}}
.x{{font-size:{28 if foto else 34}px;line-height:1.45;margin-top:18px}}
.leg{{padding:24px 64px 34px;font-size:17px;line-height:1.5;color:#5f676d;border-top:2px solid #dfeef0;margin-top:30px}}"""
    cuerpo = f"""<div class=w><div class=h>{svg_inline("clinmet_logo", "330px")}<div style="font-weight:700;color:{TEAL_OSC};font-size:24px">WhatsApp {WA_VISIBLE}</div></div>
{foto_html}<div class=b>{"" if foto else '<div class=wm>' + svg_inline("clinmet_icono", "380px") + '</div>'}<div class=k>{kicker}</div><h1>{titulo}</h1><div class=x>{texto}</div></div>
<div class=leg><i>{LEYENDA}</i> {DOCTOR}. {NUTRI}. Aviso de publicidad COFEPRIS {AVISO_PUB}.</div></div>"""
    return pagina(cuerpo, "1080px", "1350px", extra)


POSTS = {
    "post_equipo": dict(kicker="CONOCE A TU EQUIPO", titulo='Un médico y un nutriólogo, <span class=t>en persona</span>',
                        texto="Dr. Luis Alejandro López Valenzuela y Ln. César Alfredo Romero Palafox. Tu programa de control de peso empieza con una valoración presencial.",
                        foto="equipo.png", recorte="center 22%"),
    "post_donde": dict(kicker="DÓNDE ESTAMOS", titulo='Consultorio 7, <span class=t>Clínica Santa Elena</span>',
                       texto="Av. Guerrero 826, Col. Del Valle, Cd. Obregón.<br>" + HORARIO + ".",
                       foto="doctor_recepcion.png", recorte="center 35%"),
    "post_programa": dict(kicker="PROGRAMA MÉDICO DE CONTROL DE PESO", titulo='Primero te <span class=t>valoramos</span>. Después, tu plan.',
                          texto="1. Valoración médica presencial<br>2. Estudios de laboratorio<br>3. Plan con nutriólogo y seguimiento<br><br>Si un tratamiento con medicamento está indicado para ti, lo decide el médico en tu consulta."),
    "post_valoracion": dict(kicker="AGENDA POR WHATSAPP", titulo='Tu valoración, <span class=t>sin rodeos</span>',
                            texto=f"Escríbenos al {WA_VISIBLE}. Te damos horario, te explicamos el programa y lo que incluye la valoración."),
}


def main():
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        def guardar(nombre, html, w, h, escala=1, pdf=None):
            f = OUT / f"{nombre}.html"
            f.write_text(html, encoding="utf-8")
            pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=escala)
            pg.goto(f.as_uri()); pg.wait_for_timeout(400)
            pg.screenshot(path=str(OUT / f"{nombre}.png"))
            if pdf:
                pg.pdf(path=str(OUT / f"{nombre}.pdf"), width=pdf[0], height=pdf[1], print_background=True, page_ranges="1")
            pg.close()
        # banner: vista previa y PDF a tamaño real 80x200 cm (vectorial: texto, logo y QR no se pixelean)
        # PDF vectorial en proporción 80:200 (800x2000 px); la imprenta lo escala a 80x200 cm sin perder calidad
        guardar("banner_80x200", banner(), 800, 2000, 1, ("800px", "2000px"))
        # versión para laboratorios (Licea): layout de César ("¿Cómo está tu salud metabólica?")
        guardar("banner_laboratorio_80x200", banner_metabolico(), 800, 2000, 1, ("800px", "2000px"))
        mm = 96 / 25.4
        guardar("tarjeta_frente", tarjeta_frente(), int(90 * mm), int(50 * mm), 4, ("90mm", "50mm"))
        guardar("tarjeta_doctor", tarjeta_reverso("Dr. Luis Alejandro López Valenzuela", "Médico general · Diplomado en Bariatría clínica",
                                                  "Médico general · Universidad Santander · Cédula profesional 14747768"),
                int(90 * mm), int(50 * mm), 4, ("90mm", "50mm"))
        guardar("tarjeta_nutriologo", tarjeta_reverso("Ln. César Alfredo Romero Palafox", "Nutriólogo",
                                                      "Nutriólogo · Universidad La Salle Noroeste · Cédula profesional 11230740 · "
                                                      "Consultorio médico del Dr. Luis Alejandro López Valenzuela"),
                int(90 * mm), int(50 * mm), 4, ("90mm", "50mm"))
        for k, v in POSTS.items():
            guardar(k, post(**v), 1080, 1350)
        b.close()
    print("ok")


if __name__ == "__main__":
    main()
