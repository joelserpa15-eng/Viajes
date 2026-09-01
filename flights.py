#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente ligero de la API de Amadeus para obtener precios REALES de vuelos
ida y vuelta y la aerolínea más económica.

No requiere dependencias externas (usa urllib). Si no hay credenciales o la
API falla, las funciones devuelven None y el generador usa sus estimaciones
como respaldo.

Variables de entorno:
  AMADEUS_API_KEY     (obligatoria para precios reales)
  AMADEUS_API_SECRET  (obligatoria para precios reales)
  AMADEUS_ENV         "test" (por defecto) o "production"

Documentación: https://developers.amadeus.com
Endpoints usados:
  POST /v1/security/oauth2/token   (OAuth2 client_credentials)
  GET  /v2/shopping/flight-offers  (Flight Offers Search)
"""

import os
import json
import time
import urllib.parse
import urllib.request
import urllib.error

_BASES = {
    "test": "https://test.api.amadeus.com",
    "production": "https://api.amadeus.com",
}

_CACHE_FILE = os.path.join("_cache", "flights.json")
_CACHE_TTL = 60 * 60 * 24 * 3  # 3 días: evita gastar cuota en re-ejecuciones


def credentials_present() -> bool:
    return bool(os.environ.get("AMADEUS_API_KEY") and os.environ.get("AMADEUS_API_SECRET"))


def _base() -> str:
    return _BASES.get(os.environ.get("AMADEUS_ENV", "test"), _BASES["test"])


# ---------------------------------------------------------------- caché disco
def _load_cache() -> dict:
    try:
        with open(_CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_cache(cache: dict) -> None:
    os.makedirs(os.path.dirname(_CACHE_FILE), exist_ok=True)
    with open(_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=0)


# ------------------------------------------------------------------- auth
_token_cache = {"token": None, "exp": 0}


def _get_token() -> str | None:
    if _token_cache["token"] and time.time() < _token_cache["exp"] - 30:
        return _token_cache["token"]

    data = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": os.environ["AMADEUS_API_KEY"],
        "client_secret": os.environ["AMADEUS_API_SECRET"],
    }).encode()

    req = urllib.request.Request(
        _base() + "/v1/security/oauth2/token",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.load(resp)
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
        print(f"[flights] Error de autenticación Amadeus: {e}")
        return None

    _token_cache["token"] = payload.get("access_token")
    _token_cache["exp"] = time.time() + payload.get("expires_in", 1799)
    return _token_cache["token"]


# ------------------------------------------------------------- búsqueda
def search_roundtrip(origin, dest, dep_date, ret_date, currency="EUR"):
    """
    Devuelve (precio_eur:int, aerolinea:str) del vuelo ida y vuelta más barato,
    o None si no hay credenciales / datos / error.
    """
    if not credentials_present():
        return None

    cache = _load_cache()
    key = f"{origin}-{dest}-{dep_date}-{ret_date}-{currency}"
    hit = cache.get(key)
    if hit and time.time() - hit.get("ts", 0) < _CACHE_TTL:
        return (hit["precio"], hit["aerolinea"]) if hit.get("precio") else None

    token = _get_token()
    if not token:
        return None

    params = urllib.parse.urlencode({
        "originLocationCode": origin,
        "destinationLocationCode": dest,
        "departureDate": dep_date,
        "returnDate": ret_date,
        "adults": 1,
        "currencyCode": currency,
        "max": 10,
        "nonStop": "false",
    })
    req = urllib.request.Request(
        f"{_base()}/v2/shopping/flight-offers?{params}",
        headers={"Authorization": f"Bearer {token}"},
    )

    resultado = None
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            payload = json.load(resp)
        ofertas = payload.get("data", [])
        carriers = payload.get("dictionaries", {}).get("carriers", {})
        if ofertas:
            mejor = min(ofertas, key=lambda o: float(o["price"]["grandTotal"]))
            precio = round(float(mejor["price"]["grandTotal"]))
            codigos = mejor.get("validatingAirlineCodes") or []
            aerolinea = carriers.get(codigos[0], codigos[0]) if codigos else "—"
            aerolinea = aerolinea.title() if aerolinea.isupper() else aerolinea
            resultado = (precio, aerolinea)
    except urllib.error.HTTPError as e:
        print(f"[flights] HTTP {e.code} para {origin}->{dest}: {e.read()[:200]!r}")
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"[flights] Error consultando {origin}->{dest}: {e}")

    # Guardar en caché (incluido el "sin resultado" para no reintentar todo el rato)
    cache[key] = {
        "ts": time.time(),
        "precio": resultado[0] if resultado else None,
        "aerolinea": resultado[1] if resultado else None,
    }
    _save_cache(cache)
    return resultado
