# ClinMet — Clínica Metabólica del Noroeste

- `marca/`  logo en vector (`python3 marca/logo.py` regenera SVG y PNG)
- `piezas.py` → `piezas/`  banners 80×200, tarjetas 90×50 mm, posts 1080×1350 y textos de publicaciones
- `web/build.py` → `web/sitio/`  sitio de clinmet.com (lo único que se publica)
- `fotos/`  originales del equipo

## Publicación (servernas)
nginx (`aegis-final`) sirve `web/sitio` desde `/opt/aegis-site/clinmet-repo`:

    root /usr/share/nginx/html/clinmet-repo/web/sitio;

Actualizar: `cd /opt/aegis-site/clinmet-repo && git pull`

Toda pieza publicitaria lleva la leyenda "Cada paciente requiere valoración médica. Los resultados varían.",
cédulas e institución de doctor y nutriólogo y el aviso de publicidad COFEPRIS. Sin nombres de medicamentos,
sin fotos de antes/después y sin testimonios.
