package com.serpa.gastosmensuales.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.AssistChip
import androidx.compose.material3.Card
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.serpa.gastosmensuales.data.Category
import com.serpa.gastosmensuales.data.Expense

@Composable
fun PendingExpensesSection(
    pending: List<Expense>,
    onCategorize: (Expense, Category) -> Unit,
    onDiscard: (Expense) -> Unit
) {
    if (pending.isEmpty()) return

    Column {
        Text(
            text = "Pagos detectados en Google Pay sin clasificar",
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Bold
        )
        pending.forEach { expense ->
            Card(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                Column(modifier = Modifier.padding(12.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Text(text = "%.2f €".format(expense.amount), fontWeight = FontWeight.Bold)
                            Text(text = expense.description, style = MaterialTheme.typography.bodySmall)
                        }
                        IconButton(onClick = { onDiscard(expense) }) {
                            Icon(Icons.Default.Delete, contentDescription = "Descartar")
                        }
                    }
                    Row(
                        modifier = Modifier.padding(top = 8.dp),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Category.entries.forEach { category ->
                            AssistChip(
                                onClick = { onCategorize(expense, category) },
                                label = { Text(category.displayName) }
                            )
                        }
                    }
                }
            }
        }
    }
}
