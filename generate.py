#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del planificador de destinos europeos coste-efectivos desde España.

Se ejecuta automáticamente el día 1 de cada mes (vía GitHub Actions) y produce
un index.html con la planificación de los PRÓXIMOS 12 MESES, organizada en
acordeones (uno por mes). Cada mes incluye:
  - Ranking de destinos por relación calidad-precio para ese mes.
  - Presupuestos de viaje para 5, 7, 10, 15 y 20 días.
  - Precio del vuelo ida y vuelta (real vía Amadeus, o estimado) y aerolínea.
  - Recomendaciones de temporada y avisos de descuentos/eventos del mes.

Uso:
    python generate.py            # genera index.html (12 meses desde hoy)
"""

import os
import html
from datetime import datetime, timezone, timedelta, date

from data.destinos import DESTINOS
import flights

ORIGEN = os.environ.get("ORIGEN_IATA", "MAD")
MESES_ADELANTE = int(os.environ.get("MESES_ADELANTE", "12"))

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


def fechas_para_mes(base_date: date, offset: int) -> tuple[date, date]:
    """Fechas de referencia (salida ~el 15, regreso +7 días) para el mes
    situado 'offset' meses por delante de base_date. Para el mes en curso nunca
    antes de 14 días vista (las tarifas de última hora no son representativas)."""
    total = (base_date.month - 1) + offset
    anio = base_date.year + total // 12
    mes = total % 12 + 1
    salida = date(anio, mes, 15)
    earliest = base_date + timedelta(days=14)
    if salida < earliest:
        salida = earliest
    regreso = salida + timedelta(days=7)
    return salida, regreso


def meses_proximos(base_date: date, n: int) -> list:
    """Lista de periodos {offset, mes, anio, salida, regreso} para n meses."""
    periodos = []
    for off in range(n):
        salida, regreso = fechas_para_mes(base_date, off)
        total = (base_date.month - 1) + off
        periodos.append({
            "offset": off,
            "mes": total % 12 + 1,
            "anio": base_date.year + total // 12,
            "salida": salida,
            "regreso": regreso,
        })
    return periodos


def enriquecer_con_precios_reales(destinos: list, periodos: list) -> bool:
    """
    Consulta a Amadeus el vuelo i/v más barato para cada destino en CADA mes
    y guarda el resultado por mes en el destino. Devuelve True si se usó al
    menos un precio real. Sin credenciales o ante un fallo, se usa la
    estimación correspondiente como respaldo.
    """
    if not flights.credentials_present():
        print("[generate] Sin credenciales Amadeus: se usan estimaciones.")
        return False

    cotizaciones = 0
    for p in periodos:
        dep, ret = p["salida"].isoformat(), p["regreso"].isoformat()
        for d in destinos:
            if not d.get("iata"):
                continue
            res = flights.search_roundtrip(ORIGEN, d["iata"], dep, ret)
            if res:
                d.setdefault("_vuelo_real", {})[p["mes"]] = res[0]
                d.setdefault("_aerolinea_real", {})[p["mes"]] = res[1]
                cotizaciones += 1
    print(f"[generate] Precios reales aplicados: {cotizaciones} cotizaciones "
          f"en {len(periodos)} meses (origen {ORIGEN}).")
    return cotizaciones > 0


def precio_vuelo(dest: dict, mes: int) -> int:
    reales = dest.get("_vuelo_real", {})
    if mes in reales:
        return reales[mes]  # ya refleja la temporada (fechas reales)
    return round(dest["vuelo_base"] * MULT_VUELO_MES[mes])


def aerolinea_de(dest: dict, mes: int) -> str:
    return dest.get("_aerolinea_real", {}).get(mes) or dest["aerolinea"]


def es_precio_real(dest: dict, mes: int) -> bool:
    return mes in dest.get("_vuelo_real", {})


def coste_dia(dest: dict, mes: int) -> int:
    return round(dest["coste_dia"] * MULT_DIA_MES[mes])


def presupuestos(dest: dict, mes: int) -> dict:
    """Presupuesto total por persona = vuelo + (coste_dia * días)."""
    vuelo = precio_vuelo(dest, mes)
    dia = coste_dia(dest, mes)
    return {d: vuelo + dia * d for d in DURACIONES}


def puntuacion(dest: dict, mes: int) -> float:
    """
    Puntúa la relación calidad-precio para el mes. Menor coste total (vuelo +
    7 días) => mejor. Si el mes está entre los 'meses_ideales' del destino,
    aplicamos una bonificación por clima/temporada.
    """
    score = presupuestos(dest, mes)[7]
    if mes in dest["meses_ideales"]:
        score *= 0.82
    return score


def fmt_eur(valor: int) -> str:
    return f"{valor:,}".replace(",", ".") + " €"


def render_seccion_mes(p: dict, abierto: bool) -> str:
    """Devuelve el bloque <details> (acordeón) de un mes."""
    mes, anio = p["mes"], p["anio"]
    destinos = sorted(DESTINOS, key=lambda d: puntuacion(d, mes))
    estacion = estacion_de(mes)
    mes_nombre = MESES_ES[mes - 1].capitalize()
    eventos = EVENTOS_MES.get(mes, [])
    rango = f"{p['salida'].strftime('%d/%m/%Y')} – {p['regreso'].strftime('%d/%m/%Y')}"
    mejor = destinos[0]

    tarjetas = []
    for i, d in enumerate(destinos, start=1):
        presu = presupuestos(d, mes)
        vuelo = precio_vuelo(d, mes)
        dia = coste_dia(d, mes)
        ideal = "✅ Temporada ideal" if mes in d["meses_ideales"] else "🟡 Temporada media/baja"
        etiqueta_precio = "🟢 real" if es_precio_real(d, mes) else "≈ estimado"
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
            <li>✈️ <strong>Vuelo i/v:</strong> {fmt_eur(vuelo)} <span class="muted">({html.escape(d['aeropuertos'])}) · {etiqueta_precio}</span></li>
            <li>🏷️ <strong>Más económico con:</strong> {html.escape(aerolinea_de(d, mes))}</li>
            <li>💶 <strong>Gasto diario aprox.:</strong> {fmt_eur(dia)}/día · <span class="muted">Moneda: {html.escape(d['moneda'])}</span></li>
          </ul>
          <table class="presu">
            <thead><tr><th>Duración</th><th>Presupuesto total / persona</th></tr></thead>
            <tbody>{filas}</tbody>
          </table>
          <p class="notas">{html.escape(d['notas'])}</p>
        </article>""")

    top = destinos[:3]
    top_items = "".join(
        f"<li><strong>{html.escape(d['nombre'])}</strong> ({html.escape(d['pais'])}) — "
        f"desde {fmt_eur(presupuestos(d, mes)[5])} por 5 días</li>"
        for d in top
    )
    eventos_items = "".join(f"<li>{html.escape(e)}</li>" for e in eventos)
    abierto_attr = " open" if abierto else ""

    return f"""
    <details class="mes"{abierto_attr}>
      <summary>
        <span class="mes-nombre">{mes_nombre} {anio}</span>
        <span class="mes-meta">{html.escape(estacion)} · mejor opción: {html.escape(mejor['nombre'])} desde {fmt_eur(presupuestos(mejor, mes)[5])}/5 días</span>
      </summary>
      <div class="mes-body">
        <p class="sub">Presupuestos por persona · fechas de referencia: {rango}</p>

        <section class="panel top">
          <h3>🏆 Mejores opciones de {mes_nombre} (calidad-precio)</h3>
          <ul class="clean">{top_items}</ul>
        </section>

        <section class="panel deals">
          <h3>🔔 Temporada y descuentos de {mes_nombre}</h3>
          <ul class="clean">{eventos_items}</ul>
        </section>

        <h3 class="rank-title">📋 Ranking completo de destinos</h3>
        <div class="grid">
          {''.join(tarjetas)}
        </div>
      </div>
    </details>"""


def render_pagina(base_date: date, hay_reales: bool) -> str:
    periodos = meses_proximos(base_date, MESES_ADELANTE)
    actualizado = base_date.strftime("%d/%m/%Y")
    desde = MESES_ES[periodos[0]["mes"] - 1].capitalize()
    hasta_p = periodos[-1]
    hasta = f"{MESES_ES[hasta_p['mes'] - 1].capitalize()} {hasta_p['anio']}"
    fuente = ("Precios de vuelo <strong>reales</strong> vía Amadeus"
              if hay_reales else
              "Precios de vuelo <strong>estimados</strong> (sin API conectada)")

    secciones = "".join(
        render_seccion_mes(p, abierto=(i == 0))
        for i, p in enumerate(periodos)
    )

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Planificador de los próximos 12 meses con los destinos de viaje más coste-efectivos de Europa desde España. Presupuestos para 5, 7, 10, 15 y 20 días, vuelos y aerolíneas más baratas, organizados por mes.">
<title>Planificador de viajes a Europa — próximos 12 meses</title>
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
  .toolbar {{ text-align:center; margin:14px 0 4px; }}
  .toolbar button {{ background:var(--card); color:var(--text); border:1px solid var(--line);
            border-radius:999px; padding:7px 16px; font-size:.9rem; cursor:pointer; margin:0 4px; }}
  .toolbar button:hover {{ border-color:var(--accent2); }}

  details.mes {{ background:var(--card); border:1px solid var(--line); border-radius:14px;
            margin:12px 0; overflow:hidden; }}
  details.mes[open] {{ border-color:var(--accent2); }}
  summary {{ cursor:pointer; padding:15px 18px; list-style:none; display:flex;
            flex-wrap:wrap; align-items:baseline; gap:6px 14px; justify-content:space-between; }}
  summary::-webkit-details-marker {{ display:none; }}
  .mes-nombre {{ font-size:1.25rem; font-weight:700; }}
  .mes-nombre::before {{ content:"▸"; color:var(--accent2); margin-right:9px; display:inline-block; }}
  details.mes[open] .mes-nombre::before {{ content:"▾"; }}
  .mes-meta {{ color:var(--muted); font-size:.9rem; }}
  .mes-body {{ padding:0 18px 22px; }}

  .panel {{ background:#0f1b30; border:1px solid var(--line); border-radius:14px;
            padding:14px 18px; margin:14px 0; }}
  .panel h3 {{ margin-top:0; font-size:1.05rem; }}
  .panel.deals {{ border-color:var(--accent); }}
  .panel.top {{ border-color:var(--accent2); }}
  ul.clean {{ margin:.2em 0; padding-left:1.2em; }}
  .rank-title {{ margin:14px 2px 8px; font-size:1.05rem; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:16px; }}
  .card {{ background:#0f1b30; border:1px solid var(--line); border-radius:14px; padding:16px 18px; }}
  .card.destacado {{ border-color:var(--accent2); box-shadow:0 0 0 1px var(--accent2) inset; }}
  .card header {{ display:flex; align-items:baseline; gap:10px; }}
  .card h3 {{ margin:.2em 0; font-size:1.15rem; }}
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
    <span class="badge">Planificación {desde} {periodos[0]['anio']} → {hasta}</span>
    <h1>Planificador de viajes a Europa coste-efectivos desde España</h1>
    <p class="sub">Los próximos {MESES_ADELANTE} meses, mes a mes · Presupuestos por persona para 5, 7, 10, 15 y 20 días · Última actualización: {actualizado}</p>
    <p class="sub">{fuente} · Origen: {html.escape(ORIGEN)}</p>
  </header>

  <div class="toolbar">
    <button type="button" onclick="document.querySelectorAll('details.mes').forEach(d=>d.open=true)">Expandir todos</button>
    <button type="button" onclick="document.querySelectorAll('details.mes').forEach(d=>d.open=false)">Contraer todos</button>
  </div>

  {secciones}

  <footer>
    <p>Los <strong>precios de vuelo</strong> marcados como 🟢 real proceden de la API de Amadeus
    (vuelo i/v más barato, 1 adulto, según las fechas de referencia de cada mes); los marcados como
    ≈ estimado son aproximaciones basadas en tarifas históricas de aerolíneas de bajo coste. El
    <strong>gasto diario</strong> (alojamiento + comidas + transporte + actividades) es siempre una
    estimación por persona con perfil económico. Verifica el precio final en Skyscanner, Google
    Flights o Kiwi antes de reservar.</p>
    <p>Esta página se regenera automáticamente el día 1 de cada mes, avanzando siempre la ventana de 12 meses.</p>
  </footer>
</div>
</body>
</html>"""


def main():
    base_date = datetime.now(timezone.utc).date()
    periodos = meses_proximos(base_date, MESES_ADELANTE)
    hay_reales = enriquecer_con_precios_reales(DESTINOS, periodos)
    pagina = render_pagina(base_date, hay_reales)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(pagina)
    print(f"index.html generado: {MESES_ADELANTE} meses desde {base_date.isoformat()}.")


if __name__ == "__main__":
    main()
