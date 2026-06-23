# -*- coding: utf-8 -*-
"""
Catálogo de destinos de todo el mundo coste-efectivos desde España.

Cada destino incluye:
  - iata:        código IATA del aeropuerto de destino (para la API de vuelos).
                 Si es None, no se consulta la API y se usa la estimación.
  - vuelo_base:  precio ORIENTATIVO de un vuelo ida y vuelta en temporada baja
                 desde Madrid (MAD), en euros. Sirve de RESPALDO si la API
                 de precios reales no está disponible.
  - aerolinea:   compañía con la que suele salir más económico (respaldo).
  - coste_dia:   gasto diario por persona con perfil "mochilero/económico"
                 (alojamiento en hostal o hotel económico + comidas +
                 transporte local + alguna actividad), en euros.
  - meses_ideales: meses (1-12) con mejor relación clima/precio.
  - moneda:      moneda local (útil para saber si hay ventaja de cambio).
  - notas:       contexto sobre el destino.

Cuando hay credenciales de la API de vuelos configuradas (ver README), el
generador sustituye 'vuelo_base' y 'aerolinea' por el PRECIO REAL más barato
y la aerolínea correspondiente para las fechas del mes en curso.
"""

DESTINOS = [
    {
        "nombre": "Lisboa",
        "pais": "Portugal",
        "iata": "LIS",
        "aeropuertos": "MAD → LIS",
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
        "iata": "OPO",
        "aeropuertos": "MAD → OPO",
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
        "iata": "FCO",
        "aeropuertos": "MAD → FCO",
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
        "iata": "NAP",
        "aeropuertos": "MAD → NAP",
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
        "iata": "BUD",
        "aeropuertos": "MAD → BUD",
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
        "iata": "PRG",
        "aeropuertos": "MAD → PRG",
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
        "iata": "KRK",
        "aeropuertos": "MAD → KRK",
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
        "iata": "OTP",
        "aeropuertos": "MAD → OTP",
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
        "iata": "SOF",
        "aeropuertos": "MAD → SOF",
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
        "iata": "ATH",
        "aeropuertos": "MAD → ATH",
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
        "iata": "SPU",
        "aeropuertos": "MAD → SPU",
        "vuelo_base": 75,
        "aerolinea": "Ryanair / Vueling",
        "coste_dia": 60,
        "meses_ideales": [5, 6, 9, 10],
        "moneda": "EUR",
        "notas": "Costa dálmata, playas e islas. Mejor en mayo-junio o "
                 "septiembre para esquivar la masificación de agosto.",
    },
    {
        "nombre": "Varsovia",
        "pais": "Polonia",
        "iata": "WAW",
        "aeropuertos": "MAD → WAW",
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
        "iata": "TIA",
        "aeropuertos": "MAD → TIA",
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
        "iata": "MLA",
        "aeropuertos": "MAD → MLA",
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
        "iata": "EDI",
        "aeropuertos": "MAD → EDI",
        "vuelo_base": 60,
        "aerolinea": "Ryanair / easyJet",
        "coste_dia": 85,
        "meses_ideales": [5, 6, 7, 8],
        "moneda": "GBP",
        "notas": "Más caro de vida, pero vuelos baratos. Agosto vive el festival "
                 "Fringe (más ambiente, pero alojamiento más caro).",
    },
    {
        "nombre": "Viena",
        "pais": "Austria",
        "iata": "VIE",
        "aeropuertos": "MAD → VIE",
        "vuelo_base": 70,
        "aerolinea": "Ryanair / Vueling",
        "coste_dia": 75,
        "meses_ideales": [4, 5, 6, 9, 10, 12],
        "moneda": "EUR",
        "notas": "Elegante y muy bien conectada. En diciembre, de los mejores "
                 "mercados navideños de Europa.",
    },

    # ----------------------------------------------------------------- ÁFRICA
    {
        "nombre": "Marrakech",
        "pais": "Marruecos",
        "iata": "RAK",
        "aeropuertos": "MAD → RAK",
        "vuelo_base": 85,
        "aerolinea": "Ryanair / Royal Air Maroc",
        "coste_dia": 38,
        "meses_ideales": [3, 4, 5, 10, 11],
        "moneda": "MAD",
        "notas": "Escapada exótica a 3 h de vuelo: zocos, riads económicos y "
                 "gastronomía. Evita el verano por el calor extremo.",
    },
    {
        "nombre": "El Cairo",
        "pais": "Egipto",
        "iata": "CAI",
        "aeropuertos": "MAD → CAI",
        "vuelo_base": 240,
        "aerolinea": "EgyptAir / Turkish",
        "coste_dia": 38,
        "meses_ideales": [10, 11, 12, 1, 2, 3, 4],
        "moneda": "EGP",
        "notas": "Pirámides de Giza y cruceros baratos por el Nilo. Mejor en "
                 "otoño-invierno; el verano es asfixiante.",
    },
    {
        "nombre": "Ciudad del Cabo",
        "pais": "Sudáfrica",
        "iata": "CPT",
        "aeropuertos": "MAD → CPT (escala)",
        "vuelo_base": 620,
        "aerolinea": "Turkish / Qatar (escala)",
        "coste_dia": 55,
        "meses_ideales": [11, 12, 1, 2, 3],
        "moneda": "ZAR",
        "notas": "De las ciudades más bellas del mundo. Verano austral (nov-mar) "
                 "y cambio muy favorable con el rand.",
    },
    {
        "nombre": "Zanzíbar",
        "pais": "Tanzania",
        "iata": "ZNZ",
        "aeropuertos": "MAD → ZNZ (escala)",
        "vuelo_base": 600,
        "aerolinea": "Turkish / Qatar (escala)",
        "coste_dia": 50,
        "meses_ideales": [6, 7, 8, 9, 1, 2],
        "moneda": "TZS",
        "notas": "Playas paradisíacas e islas de especias a precio asensible "
                 "fuera de la temporada de lluvias.",
    },
    {
        "nombre": "Nairobi",
        "pais": "Kenia",
        "iata": "NBO",
        "aeropuertos": "MAD → NBO (escala)",
        "vuelo_base": 560,
        "aerolinea": "Qatar / Turkish (escala)",
        "coste_dia": 55,
        "meses_ideales": [1, 2, 6, 7, 8, 9, 10],
        "moneda": "KES",
        "notas": "Base para safaris en Masái Mara. Mejor en la estación seca, "
                 "cuando la fauna se concentra y los precios bajan.",
    },
    {
        "nombre": "Dakar",
        "pais": "Senegal",
        "iata": "DSS",
        "aeropuertos": "MAD → DSS",
        "vuelo_base": 340,
        "aerolinea": "Iberia / Air Senegal",
        "coste_dia": 45,
        "meses_ideales": [11, 12, 1, 2, 3, 4, 5],
        "moneda": "XOF",
        "notas": "África occidental vibrante con vuelo relativamente corto y "
                 "directo. Música, playas e isla de Gorée.",
    },

    # ---------------------------------------------------- ORIENTE MEDIO / CÁUCASO
    {
        "nombre": "Estambul",
        "pais": "Turquía",
        "iata": "IST",
        "aeropuertos": "MAD → IST",
        "vuelo_base": 120,
        "aerolinea": "Turkish / Pegasus",
        "coste_dia": 45,
        "meses_ideales": [4, 5, 6, 9, 10, 11],
        "moneda": "TRY",
        "notas": "Puente entre Europa y Asia: bazares, mezquitas y gastronomía. "
                 "Cambio muy favorable con la lira.",
    },
    {
        "nombre": "Dubái",
        "pais": "Emiratos Árabes Unidos",
        "iata": "DXB",
        "aeropuertos": "MAD → DXB",
        "vuelo_base": 400,
        "aerolinea": "Emirates / flydubai",
        "coste_dia": 95,
        "meses_ideales": [11, 12, 1, 2, 3],
        "moneda": "AED",
        "notas": "Lujo y modernidad con ofertas de vuelo frecuentes. Caro de "
                 "vida; evita el verano por el calor extremo.",
    },
    {
        "nombre": "Amán",
        "pais": "Jordania",
        "iata": "AMM",
        "aeropuertos": "MAD → AMM (escala)",
        "vuelo_base": 250,
        "aerolinea": "Royal Jordanian / Turkish",
        "coste_dia": 45,
        "meses_ideales": [3, 4, 5, 9, 10, 11],
        "moneda": "JOD",
        "notas": "Base para Petra, Wadi Rum y el mar Muerto. Primavera y otoño "
                 "ofrecen el mejor clima.",
    },
    {
        "nombre": "Tiflis",
        "pais": "Georgia",
        "iata": "TBS",
        "aeropuertos": "MAD → TBS (escala)",
        "vuelo_base": 240,
        "aerolinea": "Wizz Air / Turkish",
        "coste_dia": 38,
        "meses_ideales": [5, 6, 9, 10],
        "moneda": "GEL",
        "notas": "El Cáucaso económico: vino, montañas y casco antiguo. De los "
                 "destinos con mejor relación calidad-precio del mundo.",
    },

    # ------------------------------------------------------------------- ASIA
    {
        "nombre": "Bangkok",
        "pais": "Tailandia",
        "iata": "BKK",
        "aeropuertos": "MAD → BKK (escala)",
        "vuelo_base": 500,
        "aerolinea": "Qatar / Emirates (escala)",
        "coste_dia": 35,
        "meses_ideales": [11, 12, 1, 2],
        "moneda": "THB",
        "notas": "Puerta a Tailandia y al Sudeste Asiático. Comida callejera "
                 "baratísima y excelente; estación seca nov-feb.",
    },
    {
        "nombre": "Bali",
        "pais": "Indonesia",
        "iata": "DPS",
        "aeropuertos": "MAD → DPS (escala)",
        "vuelo_base": 650,
        "aerolinea": "Qatar / Emirates (escala)",
        "coste_dia": 35,
        "meses_ideales": [4, 5, 6, 7, 8, 9],
        "moneda": "IDR",
        "notas": "Playas, arrozales y bienestar a bajo coste. Estación seca de "
                 "abril a octubre.",
    },
    {
        "nombre": "Hanói",
        "pais": "Vietnam",
        "iata": "HAN",
        "aeropuertos": "MAD → HAN (escala)",
        "vuelo_base": 550,
        "aerolinea": "Qatar / Turkish (escala)",
        "coste_dia": 30,
        "meses_ideales": [10, 11, 12, 1, 2, 3, 4],
        "moneda": "VND",
        "notas": "Norte de Vietnam y bahía de Halong. De los países más "
                 "económicos del mundo para el viajero.",
    },
    {
        "nombre": "Kuala Lumpur",
        "pais": "Malasia",
        "iata": "KUL",
        "aeropuertos": "MAD → KUL (escala)",
        "vuelo_base": 550,
        "aerolinea": "Qatar / Emirates (escala)",
        "coste_dia": 35,
        "meses_ideales": [2, 3, 6, 7, 8],
        "moneda": "MYR",
        "notas": "Hub barato del Sudeste Asiático y mezcla de culturas. Buena "
                 "base para saltar a islas y países vecinos.",
    },
    {
        "nombre": "Delhi",
        "pais": "India",
        "iata": "DEL",
        "aeropuertos": "MAD → DEL (escala)",
        "vuelo_base": 450,
        "aerolinea": "Qatar / Etihad (escala)",
        "coste_dia": 28,
        "meses_ideales": [10, 11, 12, 1, 2, 3],
        "moneda": "INR",
        "notas": "Triángulo de oro con el Taj Mahal. Coste de vida bajísimo; "
                 "mejor en los meses frescos de invierno.",
    },
    {
        "nombre": "Katmandú",
        "pais": "Nepal",
        "iata": "KTM",
        "aeropuertos": "MAD → KTM (escala)",
        "vuelo_base": 600,
        "aerolinea": "Qatar / Turkish (escala)",
        "coste_dia": 30,
        "meses_ideales": [3, 4, 10, 11],
        "moneda": "NPR",
        "notas": "Himalaya y trekking asequible. Las mejores vistas y clima en "
                 "primavera y otoño.",
    },
    {
        "nombre": "Siem Riep",
        "pais": "Camboya",
        "iata": "REP",
        "aeropuertos": "MAD → REP (escala)",
        "vuelo_base": 650,
        "aerolinea": "Qatar / Emirates (escala)",
        "coste_dia": 32,
        "meses_ideales": [11, 12, 1, 2, 3],
        "moneda": "KHR",
        "notas": "Los templos de Angkor, una de las maravillas del mundo, a "
                 "precios muy bajos. Estación seca nov-mar.",
    },
    {
        "nombre": "Colombo",
        "pais": "Sri Lanka",
        "iata": "CMB",
        "aeropuertos": "MAD → CMB (escala)",
        "vuelo_base": 550,
        "aerolinea": "Qatar / Emirates (escala)",
        "coste_dia": 35,
        "meses_ideales": [12, 1, 2, 3],
        "moneda": "LKR",
        "notas": "Playas, plantaciones de té y safaris en una isla compacta y "
                 "muy económica.",
    },
    {
        "nombre": "Tokio",
        "pais": "Japón",
        "iata": "NRT",
        "aeropuertos": "MAD → NRT (escala)",
        "vuelo_base": 700,
        "aerolinea": "Turkish / ANA (escala)",
        "coste_dia": 90,
        "meses_ideales": [3, 4, 10, 11],
        "moneda": "JPY",
        "notas": "Megaciudad fascinante; cerezos en primavera y arces en otoño. "
                 "Con el yen débil resulta más asequible de lo que parece.",
    },

    # --------------------------------------------------------------- AMÉRICA
    {
        "nombre": "Ciudad de México",
        "pais": "México",
        "iata": "MEX",
        "aeropuertos": "MAD → MEX",
        "vuelo_base": 500,
        "aerolinea": "Iberia / Aeroméxico",
        "coste_dia": 45,
        "meses_ideales": [3, 4, 11, 12],
        "moneda": "MXN",
        "notas": "Cultura, gastronomía de primer nivel y precios bajos. Gran "
                 "base para recorrer el país.",
    },
    {
        "nombre": "Cancún",
        "pais": "México",
        "iata": "CUN",
        "aeropuertos": "MAD → CUN",
        "vuelo_base": 450,
        "aerolinea": "Iberia / World2Fly",
        "coste_dia": 55,
        "meses_ideales": [12, 1, 2, 3, 4],
        "moneda": "MXN",
        "notas": "Caribe mexicano: playas, cenotes y ruinas mayas. Evita la "
                 "temporada de huracanes (sep-oct).",
    },
    {
        "nombre": "Nueva York",
        "pais": "Estados Unidos",
        "iata": "JFK",
        "aeropuertos": "MAD → JFK",
        "vuelo_base": 400,
        "aerolinea": "Iberia / Norse / United",
        "coste_dia": 130,
        "meses_ideales": [5, 6, 9, 10],
        "moneda": "USD",
        "notas": "Vuelos baratos pero ciudad cara. Primavera y otoño son lo "
                 "mejor en clima y ambiente.",
    },
    {
        "nombre": "Bogotá",
        "pais": "Colombia",
        "iata": "BOG",
        "aeropuertos": "MAD → BOG",
        "vuelo_base": 500,
        "aerolinea": "Avianca / Iberia",
        "coste_dia": 40,
        "meses_ideales": [12, 1, 2, 3],
        "moneda": "COP",
        "notas": "Puerta a Colombia: café, naturaleza y ciudades coloniales a "
                 "precios bajos.",
    },
    {
        "nombre": "Lima",
        "pais": "Perú",
        "iata": "LIM",
        "aeropuertos": "MAD → LIM",
        "vuelo_base": 650,
        "aerolinea": "Iberia / LATAM",
        "coste_dia": 40,
        "meses_ideales": [5, 6, 7, 8, 9],
        "moneda": "PEN",
        "notas": "Gastronomía de fama mundial y trampolín a Machu Picchu. "
                 "Estación seca andina de mayo a septiembre.",
    },
    {
        "nombre": "Buenos Aires",
        "pais": "Argentina",
        "iata": "EZE",
        "aeropuertos": "MAD → EZE",
        "vuelo_base": 700,
        "aerolinea": "Iberia / Aerolíneas Argentinas",
        "coste_dia": 45,
        "meses_ideales": [10, 11, 3, 4],
        "moneda": "ARS",
        "notas": "La 'París de Sudamérica', con cambio muy favorable. Primavera "
                 "y otoño australes son ideales.",
    },
    {
        "nombre": "Río de Janeiro",
        "pais": "Brasil",
        "iata": "GIG",
        "aeropuertos": "MAD → GIG",
        "vuelo_base": 600,
        "aerolinea": "Iberia / LATAM / TAP",
        "coste_dia": 50,
        "meses_ideales": [12, 1, 2, 3],
        "moneda": "BRL",
        "notas": "Playas, samba y verano austral. En febrero el Carnaval dispara "
                 "los precios: reserva con mucha antelación.",
    },
    {
        "nombre": "La Habana",
        "pais": "Cuba",
        "iata": "HAV",
        "aeropuertos": "MAD → HAV",
        "vuelo_base": 450,
        "aerolinea": "Iberia / World2Fly",
        "coste_dia": 50,
        "meses_ideales": [11, 12, 1, 2, 3, 4],
        "moneda": "CUP",
        "notas": "Un viaje en el tiempo por el Caribe. Estación seca de "
                 "noviembre a abril.",
    },
    {
        "nombre": "Santo Domingo",
        "pais": "República Dominicana",
        "iata": "SDQ",
        "aeropuertos": "MAD → SDQ",
        "vuelo_base": 450,
        "aerolinea": "Iberia / Arajet",
        "coste_dia": 50,
        "meses_ideales": [11, 12, 1, 2, 3, 4],
        "moneda": "DOP",
        "notas": "Playas caribeñas e historia colonial. Evita la temporada de "
                 "huracanes (ago-oct).",
    },

    # ------------------------------------------------------------- OCEANÍA
    {
        "nombre": "Sídney",
        "pais": "Australia",
        "iata": "SYD",
        "aeropuertos": "MAD → SYD (escala)",
        "vuelo_base": 1100,
        "aerolinea": "Qatar / Emirates (escala)",
        "coste_dia": 90,
        "meses_ideales": [10, 11, 12, 1, 2, 3],
        "moneda": "AUD",
        "notas": "Al otro lado del mundo: verano austral, playas icónicas y "
                 "naturaleza. Vuelo largo, pero experiencia única.",
    },
]
