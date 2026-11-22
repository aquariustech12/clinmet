"""Página de ClinMet (clinmet.com) — estática, para servernas (nginx aegis-final, carpeta /opt/aegis-site/clinmet).

El botón de WhatsApp va por citas.aegis-oceanit.work/w/web: el agente cuenta esos contactos como canal "Página web".
Uso: python3 build.py   → web/sitio/index.html
"""
import sys
from pathlib import Path

AQUI = Path(__file__).parent
sys.path.insert(0, str(AQUI.parent))
import piezas as P  # noqa: E402  (datos legales, colores e íconos compartidos con banner y tarjetas)

WA_WEB = "https://citas.aegis-oceanit.work/w/web"
MAPA = "https://www.google.com/maps?q=Cl%C3%ADnica+Santa+Elena,+Av.+Guerrero+826,+Col.+Del+Valle,+Ciudad+Obreg%C3%B3n,+Sonora&output=embed"
MAPA_LINK = "https://www.google.com/maps/search/?api=1&query=Cl%C3%ADnica+Santa+Elena+Guerrero+826+Ciudad+Obreg%C3%B3n"


FB_URL = "https://www.facebook.com/clinmet.obregon"
IG_URL = "https://www.instagram.com/drlopezvalenzuela/"
SVG_FB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.8 1.4-3.8 3.9v2.3H7.9v3h2.6V21z"/></svg>'
SVG_IG = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="3.5" width="17" height="17" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.2" cy="6.8" r="1.2" fill="currentColor"/></svg>'


def redes(clase):
    return (f'<div class="{clase}"><a href="{FB_URL}" target="_blank" rel="noopener" aria-label="Facebook de ClinMet">{SVG_FB}<span>Facebook</span></a>'
            f'<a href="{IG_URL}" target="_blank" rel="noopener" aria-label="Instagram @drlopezvalenzuela">{SVG_IG}<span>@drlopezvalenzuela</span></a></div>')


def ico(k, color=None, w="2"):
    return P._ico(P.ICONOS[k], color, w)


def main():
    logo = (AQUI / "sitio/img/clinmet_logo.svg").read_text().replace("<svg ", '<svg role="img" aria-label="ClinMet, Clínica Metabólica del Noroeste" ', 1)
    cond = [("glucosa", "Glucosa alta"), ("colesterol", "Colesterol elevado"), ("trigliceridos", "Triglicéridos altos"),
            ("insulina", "Resistencia a la insulina"), ("peso", "Dificultad para bajar de peso")]
    celdas = "".join(f'<li><span class=ci>{ico(k)}</span>{t}</li>' for k, t in cond)
    pasos = [("medico", "Valoración médica presencial", "El médico revisa tu historia, tu peso y tus estudios contigo, en persona."),
             ("lab", "Estudios de laboratorio", "Glucosa, perfil de lípidos y lo que tu caso necesite, para saber de dónde partimos."),
             ("manzana", "Plan con nutriólogo", "Un plan de alimentación hecho para ti, con seguimiento para ajustar lo que haga falta.")]
    pasos_html = "".join(f'<li><span class=si>{ico(k, "#fff", "2.4")}</span><h3>{t}</h3><p>{d}</p></li>' for k, t, d in pasos)
    faq = [("¿Necesito llevar estudios?", "Si ya tienes estudios recientes, tráelos. Si no, en la valoración te decimos cuáles hacen falta."),
           ("¿Cuánto cuesta la valoración?", "Escríbenos por WhatsApp y te damos el costo y los horarios disponibles."),
           ("¿Me van a dar medicamento?", "Depende de tu valoración. Si un tratamiento con medicamento está indicado para ti, lo decide el médico en tu consulta."),
           ("¿Es solo para bajar de peso?", "No. También es para quien quiere conocer y controlar su glucosa, colesterol o triglicéridos, o lleva tiempo en el gym sin ver el cambio.")]
    faq_html = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq)

    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ClinMet · Clínica Metabólica del Noroeste · Cd. Obregón</title>
<meta name="description" content="Programa médico de control de peso y salud metabólica en Ciudad Obregón: valoración médica presencial, estudios de laboratorio y plan con nutriólogo.">
<meta property="og:title" content="ClinMet · ¿Cómo está tu salud metabólica?">
<meta property="og:description" content="Médico + nutriólogo en Ciudad Obregón. Agenda tu valoración por WhatsApp.">
<meta property="og:image" content="https://clinmet.com/img/equipo.jpg">
<link rel="icon" href="/favicon.png"><link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<style>
@font-face{{font-family:P;src:url(/fonts/Poppins-Regular.ttf);font-weight:400;font-display:swap}}
@font-face{{font-family:P;src:url(/fonts/Poppins-Medium.ttf);font-weight:500;font-display:swap}}
@font-face{{font-family:P;src:url(/fonts/Poppins-Bold.ttf);font-weight:700;font-display:swap}}
:root{{--t:{P.TEAL};--to:{P.TEAL_OSC};--l:{P.LIMA};--c:{P.CIAN};--g:{P.GRIS};--f:#f3fbfc}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:P,system-ui,sans-serif;color:var(--g);background:#fff;line-height:1.55}}
a{{color:var(--to)}}
.w{{max-width:1080px;margin:0 auto;padding:0 20px}}
header{{position:sticky;top:0;z-index:5;background:rgba(255,255,255,.95);backdrop-filter:blur(6px);border-bottom:1px solid #e3f1f3}}
header .w{{display:flex;align-items:center;justify-content:space-between;height:72px}}
header .lg svg{{height:46px;width:auto;display:block}}
.btn{{display:inline-flex;align-items:center;gap:10px;background:var(--l);color:var(--g);font-weight:700;text-decoration:none;border-radius:40px;padding:14px 26px;font-size:17px}}
.btn svg{{width:24px}} .btn.o{{background:var(--to);color:#fff}}
header .btn{{padding:10px 18px;font-size:15px}}
.hero{{background:linear-gradient(180deg,var(--f),#fff);padding:56px 0 40px}}
.hero .w{{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center}}
h1{{font-size:clamp(34px,5.4vw,58px);line-height:1.08;font-weight:700}} h1 b{{color:var(--to);display:block}}
.hero p.s{{font-size:20px;margin:18px 0 28px}}
.hero .ft{{border-radius:28px;overflow:hidden;aspect-ratio:4/5;background:#dfeff1}}
.hero .ft img{{width:100%;height:100%;object-fit:cover;object-position:center 22%;display:block}}
section{{padding:56px 0}} h2{{font-size:clamp(26px,3.6vw,38px);line-height:1.15;margin-bottom:22px}}
.cds{{list-style:none;display:grid;grid-template-columns:repeat(5,1fr);gap:16px;text-align:center;font-weight:500}}
.ci{{width:86px;height:86px;margin:0 auto 10px;border-radius:50%;background:#e3f4f6;display:flex;align-items:center;justify-content:center}}.ci svg{{width:48px}}
.pill{{margin-top:28px;background:#dff2f4;border-radius:40px;padding:14px 24px;font-weight:700;text-align:center;font-size:19px}}
.band{{background:linear-gradient(135deg,var(--to),#055f6e);color:#fff;border-radius:30px;padding:36px;text-align:center}}
.band h2{{margin:0;font-size:clamp(30px,4.4vw,48px)}} .band h2 span{{color:var(--l)}} .band p{{color:#d9f1f4;font-style:italic;font-size:20px}}
.pasos{{list-style:none;display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:30px}}
.pasos li{{background:var(--f);border-radius:22px;padding:24px}}
.si{{width:64px;height:64px;border-radius:50%;background:var(--t);display:flex;align-items:center;justify-content:center;margin-bottom:12px}}.si svg{{width:36px}}
.pasos h3{{font-size:20px;line-height:1.2;margin-bottom:6px}}
.nota{{margin-top:22px;display:flex;gap:14px;align-items:center;background:#eef7f8;border-radius:18px;padding:16px 20px}}
.nota .ck{{width:42px;height:42px;border-radius:50%;background:var(--l);flex:none;display:flex;align-items:center;justify-content:center}}.ck svg{{width:26px}}
.eq{{display:grid;grid-template-columns:1fr 1fr;gap:22px}}
.eq div{{border-left:6px solid var(--l);background:var(--f);border-radius:0 18px 18px 0;padding:20px 22px}}
.eq h3{{font-size:20px}} .eq p{{font-size:15px}}
.dd{{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:stretch}}
.dd iframe{{width:100%;height:100%;min-height:320px;border:0;border-radius:22px}}
.dd .inf{{background:var(--f);border-radius:22px;padding:26px;display:flex;flex-direction:column;gap:12px}}
details{{border-bottom:1px solid #e3f1f3;padding:16px 0}} summary{{font-weight:700;cursor:pointer;font-size:18px}} details p{{margin-top:8px}}
.cta{{text-align:center;background:var(--to);color:#fff;border-radius:30px;padding:44px 24px}}
.cta h2{{color:#fff}} .cta p{{color:#d9f1f4;margin-bottom:22px}}
footer{{background:#04505c;color:#d7eef1;font-size:14px;padding:30px 0 90px;margin-top:56px}}
footer b{{color:#fff}} footer a{{color:#bfe9ef}}
.rs{{display:flex;flex-wrap:wrap;gap:10px}} .rs a{{display:inline-flex;align-items:center;gap:8px;text-decoration:none;font-weight:600;border-radius:30px;padding:8px 14px}} .rs svg{{width:22px;height:22px;flex:none}}
.inf .rs a{{background:#fff;color:var(--to);border:1.5px solid #cfe8ec}}
footer .rs{{margin-bottom:14px}} footer .rs a{{color:#fff;background:rgba(255,255,255,.12)}}
.flot{{position:fixed;right:16px;bottom:16px;z-index:9;box-shadow:0 6px 18px rgba(0,0,0,.18)}}
@media(max-width:820px){{.hero .w,.dd,.eq{{grid-template-columns:1fr}}.cds{{grid-template-columns:repeat(2,1fr)}}.cds li:last-child{{grid-column:span 2}}.pasos{{grid-template-columns:1fr}}header .btn{{display:none}}}}
</style></head><body>
<header><div class=w><a class=lg href="/">{logo}</a><a class=btn href="{WA_WEB}">{ico("wa", P.GRIS, "2.4")}Agenda tu valoración</a></div></header>

<div class=hero><div class=w><div>
<h1>¿Cómo está tu<b>salud metabólica?</b></h1>
<p class=s>Puede que no solo se trate de tu peso. En Ciudad Obregón, un médico y un nutriólogo te valoran en persona y te ayudan a entender qué necesitas.</p>
<a class=btn href="{WA_WEB}">{ico("wa", P.GRIS, "2.4")}Escríbenos por WhatsApp</a>
</div><div class=ft><img src="/img/equipo.jpg" alt="Dr. Luis Alejandro López Valenzuela y Ln. César Alfredo Romero Palafox" width="720" height="1280"></div></div></div>

<section><div class=w><h2>Conoce tus números</h2><ul class=cds>{celdas}</ul>
<div class=pill>Conoce tus números y entiende qué necesitas.</div></div></section>

<section><div class=w><div class=band><h2>Médico <span>+</span> Nutriólogo</h2><p>Una evaluación integral para ti</p></div>
<ul class=pasos>{pasos_html}</ul>
<div class=nota><span class=ck>{ico("check", "#fff", "4")}</span><div>Si un tratamiento con medicamento está indicado para ti, <b>lo decide el médico</b> en tu consulta.</div></div></div></section>

<section><div class=w><h2>Tu equipo</h2><div class=eq>
<div><h3>Dr. Luis Alejandro López Valenzuela</h3><p>Médico general · Universidad Santander · Cédula profesional 14747768 · Diplomado en Bariatría clínica</p></div>
<div><h3>Ln. César Alfredo Romero Palafox</h3><p>Nutriólogo · Universidad La Salle Noroeste · Cédula profesional 11230740</p></div>
</div></div></section>

<section><div class=w><h2>Dónde estamos</h2><div class=dd>
<iframe src="{MAPA}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa de ClinMet"></iframe>
<div class=inf><p><b>Consultorio 7, Clínica Santa Elena</b><br>Av. Guerrero 826, entre California y Quintana Roo, Col. Del Valle, Cd. Obregón, Son.</p>
<p><b>Horario</b><br>{P.HORARIO}</p><p><b>WhatsApp</b><br>{P.WA_VISIBLE}</p>
<div><b style="display:block;margin-bottom:8px">Síguenos</b>{redes("rs")}</div>
<a class="btn o" href="{MAPA_LINK}">{ico("pin", "#fff", "2.4")}Cómo llegar</a></div></div></div></section>

<section><div class=w><h2>Preguntas frecuentes</h2>{faq_html}</div></section>

<section><div class=w><div class=cta><h2>Agenda tu valoración</h2><p>Te damos horario y te explicamos el programa por WhatsApp.</p>
<a class=btn href="{WA_WEB}">{ico("wa", P.GRIS, "2.4")}Escribir por WhatsApp</a></div></div></section>

<footer><div class=w>{redes("rs")}<p><b>{P.LEYENDA}</b></p><p>{P.DOCTOR}.<br>{P.NUTRI}.</p>
<p>{P.DIRECCION}</p><p>Aviso de publicidad COFEPRIS {P.AVISO_PUB} · <a href="https://citas.aegis-oceanit.work/privacidad">Aviso de privacidad</a></p></div></footer>
<a class="btn flot" href="{WA_WEB}" aria-label="WhatsApp">{ico("wa", P.GRIS, "2.4")}WhatsApp</a>
</body></html>"""
    (AQUI / "sitio/index.html").write_text(html, encoding="utf-8")
    print("ok")


if __name__ == "__main__":
    main()
