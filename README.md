# 🌍 Viajes — Destinos de Europa más coste-efectivos desde España

Sitio web que se **actualiza automáticamente el día 1 de cada mes** con los
destinos de viaje europeos con mejor relación calidad-precio para alguien que
vive en España. Para cada destino se muestran:

- **Presupuesto total por persona** para viajes de **5, 7, 10, 15 y 20 días**.
- **Precio orientativo del vuelo** ida y vuelta y la **aerolínea más económica**.
- **Gasto diario estimado** (alojamiento económico + comidas + transporte + actividades).
- **Recomendaciones de temporada** y **avisos de descuentos/eventos** del mes.

El ranking se recalcula cada mes teniendo en cuenta la **estación** (precios de
vuelo y alojamiento suben en verano y Navidad, bajan en primavera/otoño) y el
clima ideal de cada destino.

## 🔗 El enlace que se actualiza solo

Una vez activado GitHub Pages (ver abajo), el enlace público será:

```
https://joelserpa15-eng.github.io/Viajes/
```

Ese enlace siempre mostrará la guía del mes en curso, sin que tengas que hacer nada.

## ⚙️ Cómo activar la actualización automática (una sola vez)

1. En GitHub, ve a **Settings → Pages**.
2. En **Build and deployment → Source**, elige **GitHub Actions**.
3. Listo. El flujo de trabajo `.github/workflows/update.yml`:
   - Se ejecuta **el día 1 de cada mes** (`cron: "0 5 1 * *"`).
   - También puedes lanzarlo a mano en **Actions → Actualización mensual → Run workflow**.
   - Regenera `index.html` y lo publica en GitHub Pages.

> Nota: el workflow ya tiene los permisos necesarios (`pages: write`, `id-token: write`).

## 🗂️ Estructura

| Archivo | Función |
|---|---|
| `data/destinos.py` | Catálogo de destinos con precios base, aerolíneas y estacionalidad. |
| `generate.py` | Genera `index.html` para el mes actual (ranking, presupuestos, eventos). |
| `index.html` | Página publicada (regenerada cada mes). |
| `.github/workflows/update.yml` | Automatización mensual + despliegue en Pages. |

## 🧪 Probar en local

```bash
python generate.py                 # genera index.html para el mes actual
FORCE_MONTH=12 python generate.py  # fuerza un mes concreto (1-12) para ver la estacionalidad
```

Abre `index.html` en el navegador.

## 💶 Sobre los precios

Los importes son **estimaciones** basadas en tarifas históricas de aerolíneas de
bajo coste (Ryanair, Vueling, Wizz Air, easyJet, TAP…) y costes de vida típicos.
Sirven para **comparar destinos y planificar**, no como precio de compra. Verifica
siempre el importe final en Skyscanner, Google Flights o Kiwi antes de reservar.

### (Opcional) Precios de vuelos en vivo

`generate.py` está preparado para sustituir las estimaciones por precios reales si
integras una API de vuelos (p. ej. **Skyscanner**, **Amadeus** o **Kiwi/Tequila**):

1. Añade tu clave como *secret* del repositorio (**Settings → Secrets and variables
   → Actions**), por ejemplo `FLIGHTS_API_KEY`.
2. Expón el secret en el workflow (`env: FLIGHTS_API_KEY: ${{ secrets.FLIGHTS_API_KEY }}`).
3. En `generate.py`, dentro de `precio_vuelo()`, llama a la API y usa el precio real;
   si la llamada falla, se mantiene la estimación actual como respaldo.
