package com.serpa.gastosmensuales.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AddCircle
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.serpa.gastosmensuales.data.Category
import com.serpa.gastosmensuales.ui.theme.colorForRatio

@Composable
fun CategoryColumn(
    category: Category,
    spent: Double,
    limit: Double,
    onAddClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val ratio = if (limit > 0) (spent / limit).toFloat() else 0f
    val color = colorForRatio(ratio)

    Card(
        modifier = modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
    ) {
        Column(
            modifier = Modifier.padding(12.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            Text(
                text = category.displayName,
                style = MaterialTheme.typography.labelLarge,
                fontWeight = FontWeight.Bold,
                textAlign = androidx.compose.ui.text.style.TextAlign.Center
            )
            Text(
                text = "%.2f €".format(spent),
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                color = color
            )
            Text(
                text = "de %.2f €".format(limit),
                style = MaterialTheme.typography.bodySmall
            )
            LinearProgressIndicator(
                progress = { ratio.coerceIn(0f, 1f) },
                modifier = Modifier.fillMaxWidth(),
                color = color
            )
            IconButton(onClick = onAddClick) {
                Icon(
                    imageVector = Icons.Default.AddCircle,
                    contentDescription = "Añadir gasto en ${category.displayName}"
                )
            }
        }
    }
}
