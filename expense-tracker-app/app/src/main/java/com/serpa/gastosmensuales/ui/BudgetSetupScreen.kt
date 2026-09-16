package com.serpa.gastosmensuales.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.serpa.gastosmensuales.data.MonthlyBudget

@Composable
fun BudgetSetupScreen(
    existing: MonthlyBudget?,
    onSave: (income: Double, savings: Double, basic: Double, personal: Double) -> Unit,
    onCancel: (() -> Unit)?
) {
    var income by remember { mutableStateOf(existing?.income?.toString().orEmpty()) }
    var savings by remember { mutableStateOf(existing?.savingsPercent?.toString() ?: "20") }
    var basic by remember { mutableStateOf(existing?.basicPercent?.toString() ?: "50") }
    var personal by remember { mutableStateOf(existing?.personalPercent?.toString() ?: "30") }

    val incomeValue = income.replace(",", ".").toDoubleOrNull()
    val savingsValue = savings.replace(",", ".").toDoubleOrNull() ?: 0.0
    val basicValue = basic.replace(",", ".").toDoubleOrNull() ?: 0.0
    val personalValue = personal.replace(",", ".").toDoubleOrNull() ?: 0.0
    val totalPercent = savingsValue + basicValue + personalValue
    val isValid = incomeValue != null && incomeValue > 0 && kotlin.math.abs(totalPercent - 100.0) < 0.01

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Text(
            text = "Presupuesto del mes",
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.Bold
        )
        Text(
            text = "Introduce tus ingresos y cómo quieres repartirlos. Los tres porcentajes deben sumar 100%.",
            style = MaterialTheme.typography.bodyMedium
        )

        Spacer(Modifier.height(8.dp))

        OutlinedTextField(
            value = income,
            onValueChange = { income = it },
            label = { Text("Ingresos del mes (€)") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
            modifier = Modifier.fillMaxWidth()
        )

        OutlinedTextField(
            value = savings,
            onValueChange = { savings = it },
            label = { Text("% destinado a Ahorro") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
            modifier = Modifier.fillMaxWidth()
        )

        OutlinedTextField(
            value = basic,
            onValueChange = { basic = it },
            label = { Text("% destinado a Gastos básicos") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
            modifier = Modifier.fillMaxWidth()
        )

        OutlinedTextField(
            value = personal,
            onValueChange = { personal = it },
            label = { Text("% destinado a Gastos personales") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
            modifier = Modifier.fillMaxWidth()
        )

        Text(
            text = "Total: ${"%.1f".format(totalPercent)}% ${if (isValid) "✓" else "(debe sumar 100%)"}",
            style = MaterialTheme.typography.bodyMedium,
            color = if (kotlin.math.abs(totalPercent - 100.0) < 0.01) {
                MaterialTheme.colorScheme.primary
            } else {
                MaterialTheme.colorScheme.error
            }
        )

        Spacer(Modifier.height(8.dp))

        Button(
            onClick = { onSave(incomeValue!!, savingsValue, basicValue, personalValue) },
            enabled = isValid,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Guardar presupuesto")
        }

        if (onCancel != null) {
            TextButton(onClick = onCancel, modifier = Modifier.fillMaxWidth().padding(top = 4.dp)) {
                Text("Cancelar", textAlign = androidx.compose.ui.text.style.TextAlign.Center)
            }
        }
    }
}
