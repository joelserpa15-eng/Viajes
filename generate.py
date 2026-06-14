#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de la guía mensual de destinos europeos coste-efectivos desde España.

Se ejecuta automáticamente el día 1 de cada mes (vía GitHub Actions) y produce
un index.html actualizado con:
  - Ranking de destinos por relación calidad-precio para el mes en curso.
  - Presupuestos de viaje para 5, 7, 10, 15 y 20 días.
  - Precio orientativo del vuelo ida y vuelta y aerolínea más económica.
  - Recomendaciones de temporada y avisos de descuentos/eventos del mes.

Uso:
    python generate.py            # genera index.html para el mes actual
    FORCE_MONTH=12 python generate.py   # fuerza un mes concreto (para pruebas)
"""

import os
import html
from datetime import datetime, timezone

from data.destinos import DESTINOS

DURACIONES = [5, 7, 10, 15, 20]

MESES_ES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]

ESTACIONES = {
    "Invierno": [12, 1, 2],
    "Primavera": [3, 4, 5],
    "Verano": [6, 7, 8],
    "Otoño": [9, 10, 11],
}

# Multiplicador del precio del vuelo según el mes (1.0 = temporada base).
# Verano y Navidad son los picos; primavera/otoño los valles.
MULT_VUELO_MES = {
    1: 0.85, 2: 0.85, 3: 0.95, 4: 1.05, 5: 1.05, 6: 1.25,
    7: 1.45, 8: 1.50, 9: 1.05, 10: 0.95, 11: 0.85, 12: 1.30,
}

# Multiplicador del coste diario (alojamiento) según el mes.
MULT_DIA_MES = {
    1: 0.90, 2: 0.90, 3: 0.95, 4: 1.00, 5: 1.05, 6: 1.15,
    7: 1.30, 8: 1.35, 9: 1.05, 10: 0.95, 11: 0.90, 12: 1.10,
}

# Eventos / descuentos recurrentes destacables por mes (texto informativo).
EVENTOS_MES = {
    1: [
        "Rebajas de invierno en aerolíneas: enero suele traer las tarifas "
        "más bajas del año para volar en primavera. Buen momento para reservar con antelación.",
        "Esquí asequible en Bansko (Bulgaria) y los Tatras (Polonia/Eslovaquia).",
    ],
    2: [
        "Carnaval: Venecia, Niza o Colonia disparan precios puntuales; "
        "reserva con mucha antelación o evita esas fechas.",
        "Sigue siendo temporada baja: vuelos a Centroeuropa muy económicos.",
    ],
    3: [
        "Arranca la temporada media: precios aún contenidos y buen clima en el sur de Europa.",
        "Semana Santa puede encarecer vuelos; compra con antelación si viajas en esas fechas.",
    ],
    4: [
        "Primavera plena: mejor relación clima/precio del año en Portugal, Italia y Grecia.",
        "Atención a la Semana Santa: picos de precio en torno a las fechas festivas.",
    ],
    5: [
        "Mayo es de los mejores meses: buen tiempo, menos masificación y precios moderados.",
        "Croacia y Grecia aún en temporada media antes del pico veraniego.",
    ],
    6: [
        "Empieza el alza de verano. Reserva ya cualquier viaje de julio-agosto.",
        "El Mediterráneo del Este (Albania, Grecia) ofrece mejor precio que España en costa.",
    ],
    7: [
        "Temporada alta: prioriza Europa del Este (Polonia, Rumanía, Bulgaria) para estirar el presupuesto.",
        "Reserva alojamiento con mucha antelación; los precios suben semana a semana.",
    ],
    8: [
        "Pico de precios del año. Considera ciudades del norte/este menos saturadas.",
        "Edimburgo vive el festival Fringe: mucho ambiente pero alojamiento caro.",
    ],
    9: [
        "Vuelve la temporada media: septiembre es excelente: mar templado y precios a la baja.",
        "Croacia, Grecia e Italia en su mejor momento calidad-precio tras el verano.",
    ],
    10: [
        "Otoño: de los meses más baratos para volar y con clima agradable en el sur.",
        "Malta y las islas mediterráneas siguen cálidas y a buen precio.",
    ],
    11: [
        "Temporada baja: tarifas muy competitivas a casi toda Europa.",
        "Empiezan a abrir los mercados navideños a finales de mes en Centroeuropa.",
    ],
    12: [
        "Mercados navideños: Praga, Budapest, Viena y Cracovia, mágicos pero con demanda alta.",
        "Vuela antes del 20 o después del 27 de diciembre para esquivar los picos de Navidad y Fin de Año.",
    ],
}


def estacion_de(mes: int) -> str:
    for nombre, meses in ESTACIONES.items():
        if mes in meses:
            return nombre
    return ""


def precio_vuelo(dest: dict, mes: int) -> int:
    return round(dest["vuelo_base"] * MULT_VUELO_MES[mes])


def coste_dia(dest: dict, mes: int) -> int:
    return round(dest["coste_dia"] * MULT_DIA_MES[mes])


def presupuestos(dest: dict, mes: int) -> dict:
    """Presupuesto total por persona = vuelo + (coste_dia * días)."""
    vuelo = precio_vuelo(dest, mes)
    dia = coste_dia(dest, mes)
    return {d: vuelo + dia * d for d in DURACIONES}


def puntuacion(dest: dict, mes: int) -> float:
    """
    Puntúa la relación calidad-precio para el mes en curso.
    Menor coste total (vuelo + 7 días) => mejor. Si el mes está entre los
    'meses_ideales' del destino, aplicamos una bonificación por clima/temporada.
    """
    presu_semana = presupuestos(dest, mes)[7]
    score = presu_semana
    if mes in dest["meses_ideales"]:
        score *= 0.82  # bonificación por ser temporada ideal
    return score


def fmt_eur(valor: int) -> str:
    return f"{valor:,}".replace(",", ".") + " €"


def render(mes: int, anio: int) -> str:
    destinos = sorted(DESTINOS, key=lambda d: puntuacion(d, mes))
    estacion = estacion_de(mes)
    mes_nombre = MESES_ES[mes - 1]
    actualizado = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    top = destinos[:3]
    eventos = EVENTOS_MES.get(mes, [])

    # --- Tarjetas de destino ---
    tarjetas = []
    for i, d in enumerate(destinos, start=1):
        presu = presupuestos(d, mes)
        vuelo = precio_vuelo(d, mes)
        dia = coste_dia(d, mes)
        ideal = "✅ Temporada ideal" if mes in d["meses_ideales"] else "🟡 Temporada media/baja"
        filas = "".join(
            f"<tr><td>{dias} días</td><td class='precio'>{fmt_eur(presu[dias])}</td></tr>"
            for dias in DURACIONES
        )
        destacado = " destacado" if i <= 3 else ""
        tarjetas.append(f"""
        <article class="card{destacado}">
          <header>
            <span class="rank">#{i}</span>
            <h3>{html.escape(d['nombre'])} <small>{html.escape(d['pais'])}</small></h3>
          </header>
          <p class="ideal">{ideal} · {html.escape(estacion)}</p>
          <ul class="meta">
            <li>✈️ <strong>Vuelo i/v:</strong> {fmt_eur(vuelo)} <span class="muted">({html.escape(d['aeropuertos'])})</span></li>
            <li>🏷️ <strong>Más económico con:</strong> {html.escape(d['aerolinea'])}</li>
            <li>💶 <strong>Gasto diario aprox.:</strong> {fmt_eur(dia)}/día · <span class="muted">Moneda: {html.escape(d['moneda'])}</span></li>
          </ul>
          <table class="presu">
            <thead><tr><th>Duración</th><th>Presupuesto total / persona</th></tr></thead>
            <tbody>{filas}</tbody>
          </table>
          <p class="notas">{html.escape(d['notas'])}</p>
        </article>""")

    # --- Bloque de top 3 ---
    top_items = "".join(
        f"<li><strong>{html.escape(d['nombre'])}</strong> ({html.escape(d['pais'])}) — "
        f"desde {fmt_eur(presupuestos(d, mes)[5])} por 5 días</li>"
        for d in top
    )

    # --- Eventos/descuentos ---
    eventos_items = "".join(f"<li>{html.escape(e)}</li>" for e in eventos)

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Guía mensual de los destinos de viaje más coste-efectivos de Europa desde España. Presupuestos para 5, 7, 10, 15 y 20 días, vuelos y aerolíneas más baratas.">
<title>Destinos coste-efectivos de Europa — {mes_nombre.capitalize()} {anio}</title>
<style>
  :root {{
    --bg:#0f1724; --card:#16213a; --accent:#ffd166; --accent2:#06d6a0;
    --text:#e8edf5; --muted:#9fb0c8; --line:#243352;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:linear-gradient(160deg,#0b1220,#11203a);
         color:var(--text); font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
         line-height:1.55; }}
  .wrap {{ max-width:1100px; margin:0 auto; padding:24px 18px 64px; }}
  header.hero {{ text-align:center; padding:28px 0 8px; }}
  header.hero h1 {{ font-size:clamp(1.6rem,4vw,2.6rem); margin:.2em 0; }}
  .badge {{ display:inline-block; background:var(--accent); color:#1b1300;
            font-weight:700; padding:6px 14px; border-radius:999px; font-size:.95rem; }}
  .sub {{ color:var(--muted); margin-top:6px; }}
  .panel {{ background:var(--card); border:1px solid var(--line); border-radius:16px;
            padding:18px 20px; margin:18px 0; }}
  .panel h2 {{ margin-top:0; font-size:1.15rem; }}
  .panel.deals {{ border-color:var(--accent); }}
  .panel.top {{ border-color:var(--accent2); }}
  ul.clean {{ margin:.2em 0; padding-left:1.2em; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:16px; }}
  .card {{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:16px 18px; }}
  .card.destacado {{ border-color:var(--accent2); box-shadow:0 0 0 1px var(--accent2) inset; }}
  .card header {{ display:flex; align-items:baseline; gap:10px; }}
  .card h3 {{ margin:.2em 0; font-size:1.2rem; }}
  .card h3 small {{ color:var(--muted); font-weight:500; font-size:.8em; }}
  .rank {{ background:var(--accent2); color:#00231a; font-weight:800; border-radius:8px;
           padding:2px 9px; font-size:.9rem; }}
  .ideal {{ color:var(--accent); font-weight:600; margin:.3em 0 .6em; font-size:.92rem; }}
  ul.meta {{ list-style:none; padding:0; margin:.4em 0; font-size:.94rem; }}
  ul.meta li {{ margin:.25em 0; }}
  .muted {{ color:var(--muted); font-size:.9em; }}
  table.presu {{ width:100%; border-collapse:collapse; margin:.6em 0; font-size:.94rem; }}
  table.presu th, table.presu td {{ text-align:left; padding:6px 8px; border-bottom:1px solid var(--line); }}
  table.presu th {{ color:var(--muted); font-weight:600; }}
  td.precio {{ font-weight:700; color:var(--accent); text-align:right; }}
  .notas {{ color:var(--muted); font-size:.9rem; margin:.5em 0 0; }}
  footer {{ color:var(--muted); font-size:.85rem; text-align:center; margin-top:32px; }}
  a {{ color:var(--accent2); }}
</style>
</head>
<body>
<div class="wrap">
  <header class="hero">
    <span class="badge">Actualizado: {mes_nombre.capitalize()} {anio}</span>
    <h1>Destinos de Europa más coste-efectivos desde España</h1>
    <p class="sub">Presupuestos por persona para 5, 7, 10, 15 y 20 días · Temporada: {estacion} · Última generación: {actualizado}</p>
  </header>

  <section class="panel top">
    <h2>🏆 Mejores opciones de {mes_nombre} (calidad-precio)</h2>
    <ul class="clean">{top_items}</ul>
  </section>

  <section class="panel deals">
    <h2>🔔 Temporada y descuentos de {mes_nombre}</h2>
    <ul class="clean">{eventos_items}</ul>
    <p class="muted">Consejo: las tarifas más bajas suelen aparecer reservando los vuelos con 6-10 semanas de antelación y volando martes o miércoles.</p>
  </section>

  <h2 style="margin:10px 4px;">📋 Ranking completo de destinos</h2>
  <div class="grid">
    {''.join(tarjetas)}
  </div>

  <footer>
    <p>Los precios son <strong>estimaciones</strong> basadas en tarifas históricas de aerolíneas
    de bajo coste (Ryanair, Vueling, Wizz Air, easyJet…) y costes de vida típicos por persona
    con perfil económico. Verifica siempre el precio final en buscadores como Skyscanner, Google
    Flights o Kiwi antes de reservar.</p>
    <p>Esta página se regenera automáticamente el día 1 de cada mes.</p>
  </footer>
</div>
</body>
</html>"""


def main():
    force = os.environ.get("FORCE_MONTH")
    now = datetime.now(timezone.utc)
    mes = int(force) if force else now.month
    anio = now.year
    pagina = render(mes, anio)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(pagina)
    print(f"index.html generado para {MESES_ES[mes - 1]} {anio}.")


if __name__ == "__main__":
    main()
