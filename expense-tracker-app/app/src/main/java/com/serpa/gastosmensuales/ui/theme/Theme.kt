package com.serpa.gastosmensuales.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

val GreenPrimary = Color(0xFF2E7D32)
val AmberWarning = Color(0xFFF57C00)
val RedDanger = Color(0xFFD32F2F)

private val LightColors = lightColorScheme(
    primary = GreenPrimary,
    secondary = Color(0xFF00897B)
)

private val DarkColors = darkColorScheme(
    primary = Color(0xFF66BB6A),
    secondary = Color(0xFF4DB6AC)
)

@Composable
fun GastosMensualesTheme(content: @Composable () -> Unit) {
    val colors = if (isSystemInDarkTheme()) DarkColors else LightColors
    MaterialTheme(colorScheme = colors, content = content)
}

fun colorForRatio(ratio: Float): Color = when {
    ratio >= 1f -> RedDanger
    ratio >= 0.8f -> AmberWarning
    else -> GreenPrimary
}
