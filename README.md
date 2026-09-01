# 🌍 Viajes — Destinos del mundo más coste-efectivos desde España

Sitio web que se **actualiza automáticamente el día 1 de cada mes** con la
planificación de los **próximos 12 meses**, organizada en **acordeones por mes**.
Para cada mes y cada destino del mundo (Europa, Asia, África, Oriente Medio,
América y Oceanía) con mejor relación calidad-precio para alguien que vive en
España se muestran:

- **Presupuesto total por persona** para viajes de **5, 7, 10, 15 y 20 días**.
- **Precio del vuelo** ida y vuelta (real vía Amadeus, o estimado) y la **aerolínea más económica**.
- **Gasto diario estimado** (alojamiento económico + comidas + transporte + actividades).
- **Recomendaciones de temporada** y **avisos de descuentos/eventos** del mes.

El ranking se recalcula para **cada uno de los 12 meses** teniendo en cuenta la
**estación** (precios de vuelo y alojamiento suben en verano y Navidad, bajan en
primavera/otoño) y el clima ideal de cada destino. Cada mes es un acordeón
plegable (el primero aparece abierto), y hay botones para expandir/contraer todos.

Dentro de cada mes hay **dos subdivisiones**:

- **🌍 Por el mundo:** destinos internacionales con vuelo i/v (real vía Amadeus o estimado).
- **🇪🇸 Por España:** escapadas nacionales con los **mismos criterios** (ranking, presupuestos
  por duración, mejores meses) más **cómo viajar mejor a cada sitio** (AVE, tren, autobús, vuelo
  o ferry, con duración y trucos de ahorro). El transporte nacional usa estimaciones orientativas.

## 🔗 El enlace que se actualiza solo

Una vez activado GitHub Pages (ver abajo), el enlace público será:

```
https://joelserpa15-eng.github.io/Viajes/
```

Ese enlace siempre mostrará la planificación de los 12 meses siguientes, avanzando
la ventana cada mes sin que tengas que hacer nada.

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
| `data/destinos.py` | Catálogo de destinos con códigos IATA, precios base, aerolíneas y estacionalidad. |
| `flights.py` | Cliente de la API de Amadeus (precios reales) con respaldo a estimaciones. |
| `generate.py` | Genera `index.html` con los 12 meses en acordeones (ranking, presupuestos, eventos). |
| `index.html` | Página publicada (regenerada cada mes, ventana móvil de 12 meses). |
| `.github/workflows/update.yml` | Automatización mensual + despliegue en Pages. |

## 🧪 Probar en local

```bash
python generate.py                 # genera index.html (12 meses desde hoy)
MESES_ADELANTE=6 python generate.py  # cambia el nº de meses de la ventana
```

Abre `index.html` en el navegador.

## 💶 Sobre los precios

- **Precios de vuelo:** si conectas la API de **Amadeus** (ver abajo), se usa el
  precio **real** del vuelo ida y vuelta más barato desde Madrid (1 adulto, salida
  ~3 semanas vista) y su aerolínea. Aparecen marcados como **🟢 real**. Si no hay
  API conectada, se usan **estimaciones** (marcadas como **≈ estimado**).
- **Gasto diario** (alojamiento + comidas + transporte + actividades): siempre es
  una estimación por persona con perfil económico.

Verifica siempre el importe final en Skyscanner, Google Flights o Kiwi antes de reservar.

## ✈️ Activar precios de vuelo REALES (Amadeus)

El proyecto ya está integrado con la API gratuita de **Amadeus Self-Service**.
Solo tienes que darle tus credenciales:

1. Crea una cuenta en <https://developers.amadeus.com> (gratis).
2. En **My Self-Service Workspace → Create New App**, obtén tu **API Key** y **API Secret**.
3. En GitHub, ve a **Settings → Secrets and variables → Actions → New repository secret**
   y crea estos dos *secrets*:
   - `AMADEUS_API_KEY`
   - `AMADEUS_API_SECRET`
4. (Opcional) Cuando pases de pruebas a datos de producción, crea una *variable*
   (no secret) llamada `AMADEUS_ENV` con valor `production`. Por defecto se usa el
   entorno `test`.

A partir de ahí, la actualización mensual usará precios reales automáticamente.
Si la API falla o agota la cuota, la web sigue funcionando con las estimaciones
de respaldo (nunca se rompe).

> **Entorno de pruebas (`test`):** los datos son reales pero limitados/cacheados y
> con cuota mensual reducida. Para precios totalmente al día, usa `production`.

### Probar la integración en local

```bash
export AMADEUS_API_KEY=tu_key
export AMADEUS_API_SECRET=tu_secret
python generate.py        # verás "[generate] Precios reales aplicados a N destinos"
```

Las respuestas se cachean 3 días en `_cache/` para no gastar cuota en re-ejecuciones.
