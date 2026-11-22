"""Imágenes de perfil y portada de Facebook / Instagram de ClinMet.

  redes/perfil_1080.png        foto de perfil FB e IG (se ve en círculo)
  redes/portada_facebook.png   portada 1640x924: lo importante en la franja central 1200x624
                               (escritorio recorta arriba/abajo, celular recorta los lados)
"""
from playwright.sync_api import sync_playwright

import piezas as P

OUT = P.AQUI / "redes"


def perfil() -> str:
    extra = """.w{width:1080px;height:1080px;background:#fff;display:flex;align-items:center;justify-content:center}"""
    return P.pagina(f'<div class=w>{P.svg_inline("clinmet_icono", "720px")}</div>', "1080px", "1080px", extra)


def portada() -> str:
    extra = f"""
.w{{width:1640px;height:924px;position:relative;overflow:hidden;
   background:linear-gradient(135deg,{P.TEAL_OSC} 0%,#055f6e 70%,#04505c 100%);color:#fff}}
.wm{{position:absolute;right:-90px;top:50%;transform:translateY(-50%);width:640px;opacity:.10}}
.c{{position:absolute;left:220px;right:220px;top:150px;bottom:150px;display:flex;align-items:center;gap:64px}}
.c .lg{{flex:none}}
.sep{{width:4px;align-self:stretch;margin:70px 0;background:{P.LIMA};border-radius:2px}}
h1{{font-size:64px;line-height:1.08;font-weight:700}} h1 span{{color:{P.LIMA}}}
.s{{font-size:28px;margin-top:18px;color:#d9f1f4;line-height:1.4}}
.ft{{font-size:19px;margin-top:22px;color:#bfe3e8}}"""
    cuerpo = f"""<div class=w><div class=wm>{P.svg_inline("clinmet_icono", "640px")}</div>
<div class=c><div class=lg>{P.svg_inline("clinmet_logo_vertical_blanco", "330px")}</div><div class=sep></div>
<div><h1>¿Cómo está tu<br><span>salud metabólica?</span></h1>
<div class=s>Médico + Nutriólogo · Valoración en persona<br>Consultorio 7, Clínica Santa Elena · Cd. Obregón</div>
<div class=ft>{P.LEYENDA}</div></div></div></div>"""
    return P.pagina(cuerpo, "1640px", "924px", extra)


def main():
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for nombre, html, w, h in [("perfil_1080", perfil(), 1080, 1080), ("portada_facebook", portada(), 1640, 924)]:
            f = OUT / f"{nombre}.html"
            f.write_text(html, encoding="utf-8")
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.goto(f.as_uri()); pg.wait_for_timeout(400)
            pg.screenshot(path=str(OUT / f"{nombre}.png"))
            pg.close()
        b.close()
    print("ok")


if __name__ == "__main__":
    main()
