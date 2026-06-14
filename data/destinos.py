# -*- coding: utf-8 -*-
"""
Catálogo de destinos europeos coste-efectivos desde España.

Cada destino incluye:
  - vuelo_base:  precio ORIENTATIVO de un vuelo ida y vuelta en temporada baja
                 desde un aeropuerto principal de España (MAD/BCN), en euros.
  - aerolinea:   compañía con la que suele salir más económico.
  - coste_dia:   gasto diario por persona con perfil "mochilero/económico"
                 (alojamiento en hostal o hotel económico + comidas +
                 transporte local + alguna actividad), en euros.
  - meses_ideales: meses (1-12) con mejor relación clima/precio.
  - moneda:      moneda local (útil para saber si hay ventaja de cambio).
  - notas:       contexto sobre el destino.

IMPORTANTE: los precios son estimaciones basadas en tarifas históricas de
aerolíneas de bajo coste y costes de vida típicos. El generador aplica
ajustes por temporada en cada actualización mensual. Para precios en vivo,
ver README.md (integración opcional con una API de vuelos).
"""

DESTINOS = [
    {
        "nombre": "Lisboa",
        "pais": "Portugal",
        "aeropuertos": "MAD/BCN → LIS",
        "vuelo_base": 45,
        "aerolinea": "Ryanair / TAP",
        "coste_dia": 60,
        "meses_ideales": [3, 4, 5, 6, 9, 10],
        "moneda": "EUR",
        "notas": "Vuelo corto, sin cambio de moneda y gastronomía asequible. "
                 "Ideal en primavera y otoño para evitar el calor y los precios de verano.",
    },
    {
        "nombre": "Oporto",
        "pais": "Portugal",
        "aeropuertos": "MAD/BCN → OPO",
        "vuelo_base": 40,
        "aerolinea": "Ryanair",
        "coste_dia": 55,
        "meses_ideales": [4, 5, 6, 9, 10],
        "moneda": "EUR",
        "notas": "Uno de los destinos más baratos de Europa occidental. "
                 "Vinos del Duero, casco histórico y cercanía a España.",
    },
    {
        "nombre": "Roma",
        "pais": "Italia",
        "aeropuertos": "MAD/BCN → FCO/CIA",
        "vuelo_base": 55,
        "aerolinea": "Ryanair / Vueling",
        "coste_dia": 70,
        "meses_ideales": [3, 4, 5, 10, 11],
        "moneda": "EUR",
        "notas": "Mucho que ver de forma gratuita o barata. Evita julio-agosto "
                 "por calor y precios; primavera y otoño son óptimos.",
    },
    {
        "nombre": "Nápoles",
        "pais": "Italia",
        "aeropuertos": "MAD/BCN → NAP",
        "vuelo_base": 50,
        "aerolinea": "Ryanair",
        "coste_dia": 60,
        "meses_ideales": [4, 5, 6, 9, 10],
        "moneda": "EUR",
        "notas": "Base barata para Pompeya y la Costa Amalfitana. "
                 "Comida excelente a bajo precio.",
    },
    {
        "nombre": "Budapest",
        "pais": "Hungría",
        "aeropuertos": "MAD/BCN → BUD",
        "vuelo_base": 65,
        "aerolinea": "Ryanair / Wizz Air",
        "coste_dia": 45,
        "meses_ideales": [4, 5, 6, 9, 10],
        "moneda": "HUF",
        "notas": "Excelente relación calidad-precio. Balnearios termales y "
                 "ventaja de cambio con el florín. Diciembre brilla por sus mercados navideños.",
    },
    {
        "nombre": "Praga",
        "pais": "República Checa",
        "aeropuertos": "MAD/BCN → PRG",
        "vuelo_base": 70,
        "aerolinea": "Ryanair / Vueling",
        "coste_dia": 50,
        "meses_ideales": [4, 5, 6, 9, 10, 12],
        "moneda": "CZK",
        "notas": "Cerveza y comida muy baratas, centro histórico compacto y caminable. "
                 "Mágica con nieve en diciembre.",
    },
    {
        "nombre": "Cracovia",
        "pais": "Polonia",
        "aeropuertos": "MAD/BCN → KRK",
        "vuelo_base": 55,
        "aerolinea": "Ryanair / Wizz Air",
        "coste_dia": 40,
        "meses_ideales": [5, 6, 7, 8, 9],
        "moneda": "PLN",
        "notas": "De los destinos más económicos de Europa. Excursión a "
                 "Auschwitz y a las minas de sal de Wieliczka.",
    },
    {
        "nombre": "Bucarest",
        "pais": "Rumanía",
        "aeropuertos": "MAD/BCN → OTP",
        "vuelo_base": 45,
        "aerolinea": "Wizz Air / Ryanair",
        "coste_dia": 38,
        "meses_ideales": [5, 6, 9, 10],
        "moneda": "RON",
        "notas": "El destino con el coste de vida más bajo de la lista. "
                 "Puerta de entrada a Transilvania.",
    },
    {
        "nombre": "Sofía",
        "pais": "Bulgaria",
        "aeropuertos": "MAD/BCN → SOF",
        "vuelo_base": 60,
        "aerolinea": "Wizz Air / Ryanair",
        "coste_dia": 38,
        "meses_ideales": [5, 6, 9, 10],
        "moneda": "BGN",
        "notas": "Muy barato y con montañas a un paso (Vitosha). "
                 "Esquí asequible en invierno en Bansko.",
    },
    {
        "nombre": "Atenas",
        "pais": "Grecia",
        "aeropuertos": "MAD/BCN → ATH",
        "vuelo_base": 90,
        "aerolinea": "Ryanair / Aegean",
        "coste_dia": 55,
        "meses_ideales": [4, 5, 6, 9, 10],
        "moneda": "EUR",
        "notas": "Historia milenaria y trampolín barato a las islas griegas. "
                 "Primavera y otoño evitan el calor extremo.",
    },
    {
        "nombre": "Split",
        "pais": "Croacia",
        "aeropuertos": "MAD/BCN → SPU",
        "vuelo_base": 75,
        "aerolinea": "Ryanair / Vueling",
        "coste_dia": 60,
        "meses_ideales": [5, 6, 9, 10],
        "moneda": "EUR",
        "notas": "Costa dálmata, playas e islas. Mejor en mayo-junio o "
                 "septiembre para esquivar la masificación de agosto.",
    },
    {
        "nombre": "Cracovia/Varsovia y alrededores",
        "pais": "Polonia",
        "aeropuertos": "MAD/BCN → WAW",
        "vuelo_base": 60,
        "aerolinea": "Ryanair / Wizz Air",
        "coste_dia": 42,
        "meses_ideales": [5, 6, 7, 8, 9],
        "moneda": "PLN",
        "notas": "Capital moderna y económica, buena base para recorrer Polonia en tren.",
    },
    {
        "nombre": "Tirana",
        "pais": "Albania",
        "aeropuertos": "MAD/BCN → TIA",
        "vuelo_base": 70,
        "aerolinea": "Wizz Air",
        "coste_dia": 35,
        "meses_ideales": [5, 6, 9, 10],
        "moneda": "ALL",
        "notas": "La 'Riviera albanesa' es la alternativa más barata al Mediterráneo. "
                 "Coste de vida bajísimo.",
    },
    {
        "nombre": "Valeta",
        "pais": "Malta",
        "aeropuertos": "MAD/BCN → MLA",
        "vuelo_base": 65,
        "aerolinea": "Ryanair",
        "coste_dia": 60,
        "meses_ideales": [4, 5, 6, 9, 10, 11],
        "moneda": "EUR",
        "notas": "Clima suave casi todo el año, inglés como idioma oficial y "
                 "playas. Buena opción incluso en otoño-invierno.",
    },
    {
        "nombre": "Edimburgo",
        "pais": "Reino Unido",
        "aeropuertos": "MAD/BCN → EDI",
        "vuelo_base": 60,
        "aerolinea": "Ryanair / easyJet",
        "coste_dia": 85,
        "meses_ideales": [5, 6, 7, 8],
        "moneda": "GBP",
        "notas": "Más caro de vida, pero vuelos baratos. Agosto vive el festival "
                 "Fringe (más ambiente, pero alojamiento más caro).",
    },
    {
        "nombre": "Cracovia invernal / Centroeuropa",
        "pais": "Varios",
        "aeropuertos": "MAD/BCN → varios",
        "vuelo_base": 55,
        "aerolinea": "Ryanair / Wizz Air",
        "coste_dia": 45,
        "meses_ideales": [12, 1, 2],
        "moneda": "Varias",
        "notas": "En invierno, los mercados navideños y el bajo coste hacen de "
                 "Centroeuropa la mejor opción calidad-precio.",
    },
]
