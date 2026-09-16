package com.serpa.gastosmensuales.notifications

import android.app.Notification
import android.content.Context
import android.service.notification.NotificationListenerService
import android.service.notification.StatusBarNotification
import androidx.core.app.NotificationManagerCompat
import com.serpa.gastosmensuales.GastosApplication
import com.serpa.gastosmensuales.data.ExpenseSource
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch

/**
 * Escucha las notificaciones publicadas por Google Wallet / Google Pay para detectar
 * pagos automáticamente. El usuario debe conceder el permiso "Acceso a notificaciones"
 * manualmente en Ajustes (Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS).
 *
 * Los gastos detectados se guardan sin clasificación (category = null); el usuario los
 * asigna a Ahorro / Gastos básicos / Gastos personales desde el panel principal.
 *
 * El formato del texto de la notificación varía por país e idioma, por lo que la
 * extracción del importe es heurística (busca el primer número con formato de moneda).
 */
class GooglePayNotificationListener : NotificationListenerService() {

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    override fun onNotificationPosted(sbn: StatusBarNotification) {
        if (sbn.packageName !in MONITORED_PACKAGES) return

        val extras = sbn.notification.extras
        val title = extras.getCharSequence(Notification.EXTRA_TITLE)?.toString().orEmpty()
        val text = extras.getCharSequence(Notification.EXTRA_TEXT)?.toString().orEmpty()
        val fullText = "$title $text".trim()

        val amount = extractAmount(fullText) ?: return

        val app = application as GastosApplication
        scope.launch {
            app.repository.addExpense(
                amount = amount,
                category = null,
                description = fullText.ifBlank { "Pago con Google Pay" },
                source = ExpenseSource.GOOGLE_PAY
            )
        }
    }

    companion object {
        val MONITORED_PACKAGES = setOf(
            "com.google.android.apps.walletnfcrel", // Google Wallet / Google Pay
            "com.google.android.apps.nbu.paisa.user" // Google Pay (India)
        )

        private val AMOUNT_REGEX = Regex("""[€$]?\s?(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)\s?[€$]?""")

        fun extractAmount(text: String): Double? {
            val match = AMOUNT_REGEX.find(text) ?: return null
            return normalizeNumber(match.groupValues[1]).toDoubleOrNull()
        }

        /** Normaliza "1.234,56" o "1,234.56" a "1234.56". */
        private fun normalizeNumber(raw: String): String {
            val hasComma = raw.contains(",")
            val hasDot = raw.contains(".")
            return when {
                hasComma && hasDot -> {
                    if (raw.lastIndexOf(',') > raw.lastIndexOf('.')) {
                        raw.replace(".", "").replace(",", ".")
                    } else {
                        raw.replace(",", "")
                    }
                }
                hasComma -> {
                    val decimals = raw.substringAfterLast(',')
                    if (decimals.length == 2) raw.replace(",", ".") else raw.replace(",", "")
                }
                else -> raw
            }
        }

        fun isEnabled(context: Context): Boolean =
            context.packageName in NotificationManagerCompat.getEnabledListenerPackages(context)
    }
}
