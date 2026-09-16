# 💸 Gastos Mensuales

App Android (Kotlin + Jetpack Compose) para controlar tus gastos mensuales, con
detección automática de pagos de Google Pay / Google Wallet mediante notificaciones.

## Funcionalidad

- **Configuración mensual**: al abrir la app introduces tus ingresos del mes y el
  porcentaje que quieres destinar a **Ahorro**, **Gastos básicos** (mercado,
  servicios, alquiler...) y **Gastos personales** (ocio, planes, caprichos). Los
  tres porcentajes deben sumar 100%.
- **Detección de pagos de Google Pay**: un `NotificationListenerService` escucha
  las notificaciones de Google Wallet / Google Pay, extrae el importe y las guarda
  como gasto **sin clasificar**; desde el panel principal se asignan con un toque
  a una de las tres categorías (o se descartan si no son gastos reales).
- **Panel principal desplegable**: una tarjeta muestra el total gastado del mes
  frente al presupuesto total; al pulsarla se despliega en **3 columnas** (Ahorro /
  Básicos / Personales) con el importe gastado, el límite y una barra de progreso.
  El número de gastado se pinta en **verde** (<80% del límite), **ámbar** (80-99%)
  o **rojo** (100% o más) para avisar cuando te acercas o superas el límite.
- **Alta manual de gastos**: cada columna tiene un botón "+" para añadir un gasto
  manual (importe y descripción) directamente en esa clasificación.

## Estructura

```
app/src/main/java/com/serpa/gastosmensuales/
├── MainActivity.kt
├── GastosApplication.kt
├── data/                     # Entidades Room, DAOs, base de datos y repositorio
├── notifications/            # NotificationListenerService de Google Pay
├── ui/                       # Pantallas y componentes de Jetpack Compose
├── ui/theme/                 # Tema Material 3 y lógica de colores por umbral
└── viewmodel/                # ExpenseViewModel (estado observable con StateFlow)
```

Persistencia local con **Room** (SQLite), sin backend ni conexión a internet:
todos los datos se quedan en el dispositivo.

## Permiso necesario: acceso a notificaciones

Android no permite pedir el permiso de "Acceso a notificaciones" con un diálogo
estándar. La primera vez que abras la app, si el permiso no está concedido verás
un aviso con un botón "Abrir ajustes" que te lleva directamente a
**Ajustes → Apps → Acceso especial → Acceso a notificaciones**, donde debes
activar "Gastos Mensuales" manualmente.

## Sobre la detección de importes

El texto de las notificaciones de Google Pay / Google Wallet varía según el país,
idioma y versión de la app. `GooglePayNotificationListener.extractAmount()` usa una
expresión regular heurística para localizar el primer importe con formato de
moneda (`12,34 €`, `$12.34`, etc.). Si tras probarlo en tu dispositivo detectas que
no reconoce bien tus notificaciones, ajusta la regex o añade el paquete correcto de
tu región a `MONITORED_PACKAGES` (puedes verlo con
`adb shell dumpsys notification` mientras llega un pago).

## Cómo compilar

1. Abre la carpeta `expense-tracker-app/` con **Android Studio** (Koala o
   posterior). Android Studio generará automáticamente el `gradle-wrapper.jar`
   que falta en este repositorio.
2. Deja que sincronice Gradle (usa AGP 8.5.2, Kotlin 1.9.24, compileSdk 34,
   minSdk 26).
3. Ejecuta la app en un emulador o dispositivo físico con Google Pay / Google
   Wallet instalado para probar la detección de notificaciones.

> Este entorno no tiene Android SDK ni el `gradle-wrapper.jar` binario, por lo
> que el proyecto no se ha compilado aquí; revisa que compile en Android Studio
> antes de publicar una versión.

## Posibles mejoras futuras

- Gráficas de evolución mensual e histórico de meses anteriores.
- Exportar/backup de los datos (actualmente solo locales en el dispositivo).
- Notificación propia cuando una categoría supera el límite, no solo el color.
- Editar o eliminar gastos ya registrados desde el listado del mes.
