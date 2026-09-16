package com.serpa.gastosmensuales.ui

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.filled.KeyboardArrowUp
import androidx.compose.material3.Card
import androidx.compose.material3.Icon
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
fun ExpandableSummaryCard(
    totalSpent: Double,
    totalBudget: Double,
    expanded: Boolean,
    onToggle: () -> Unit,
    categoryTotals: Map<Category, Double>,
    limits: Map<Category, Double>,
    onAddExpense: (Category) -> Unit
) {
    val ratio = if (totalBudget > 0) (totalSpent / totalBudget).toFloat() else 0f
    val color = colorForRatio(ratio)

    Card(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable(onClick = onToggle),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text(
                        text = "Gastado este mes",
                        style = MaterialTheme.typography.bodyMedium
                    )
                    Text(
                        text = "%.2f € de %.2f €".format(totalSpent, totalBudget),
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.Bold,
                        color = color
                    )
                }
                Icon(
                    imageVector = if (expanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown,
                    contentDescription = if (expanded) "Contraer" else "Expandir"
                )
            }

            AnimatedVisibility(visible = expanded) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Category.entries.forEach { category ->
                        CategoryColumn(
                            category = category,
                            spent = categoryTotals[category] ?: 0.0,
                            limit = limits[category] ?: 0.0,
                            onAddClick = { onAddExpense(category) },
                            modifier = Modifier.weight(1f)
                        )
                    }
                }
            }
        }
    }
}
