package com.serpa.gastosmensuales.ui

import android.content.Intent
import android.provider.Settings
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.unit.dp
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import com.serpa.gastosmensuales.data.Category
import com.serpa.gastosmensuales.data.MonthlyBudget
import com.serpa.gastosmensuales.notifications.GooglePayNotificationListener
import com.serpa.gastosmensuales.viewmodel.ExpenseViewModel
import java.time.YearMonth
import java.time.format.TextStyle
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DashboardScreen(
    viewModel: ExpenseViewModel,
    budget: MonthlyBudget,
    onEditBudget: () -> Unit
) {
    val context = LocalContext.current
    val categoryTotals by viewModel.categoryTotals.collectAsState()
    val pendingExpenses by viewModel.pendingExpenses.collectAsState()

    var expanded by remember { mutableStateOf(true) }
    var dialogCategory by remember { mutableStateOf<Category?>(null) }
    var notificationAccessGranted by remember { mutableStateOf(GooglePayNotificationListener.isEnabled(context)) }

    val lifecycleOwner = LocalLifecycleOwner.current
    DisposableEffect(lifecycleOwner) {
        val observer = LifecycleEventObserver { _, event ->
            if (event == Lifecycle.Event.ON_RESUME) {
                notificationAccessGranted = GooglePayNotificationListener.isEnabled(context)
            }
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose { lifecycleOwner.lifecycle.removeObserver(observer) }
    }

    val limits = Category.entries.associateWith { budget.limitFor(it) }
    val totalSpent = categoryTotals.values.sum()
    val totalBudget = limits.values.sum()

    val monthLabel = remember(viewModel) {
        val ym = YearMonth.parse(viewModel.currentMonth())
        val monthName = ym.month.getDisplayName(TextStyle.FULL, Locale("es", "ES"))
        "${monthName.replaceFirstChar { it.uppercase() }} ${ym.year}"
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Gastos · $monthLabel") },
                actions = {
                    IconButton(onClick = onEditBudget) {
                        Icon(Icons.Default.Settings, contentDescription = "Editar presupuesto")
                    }
                }
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            if (!notificationAccessGranted) {
                item {
                    Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer)) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text(
                                text = "Para registrar automáticamente tus pagos de Google Pay, concede el acceso a notificaciones.",
                                color = MaterialTheme.colorScheme.onErrorContainer
                            )
                            Button(
                                onClick = {
                                    context.startActivity(Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS))
                                },
                                modifier = Modifier.padding(top = 8.dp)
                            ) {
                                Text("Abrir ajustes")
                            }
                        }
                    }
                }
            }

            item {
                ExpandableSummaryCard(
                    totalSpent = totalSpent,
                    totalBudget = totalBudget,
                    expanded = expanded,
                    onToggle = { expanded = !expanded },
                    categoryTotals = categoryTotals,
                    limits = limits,
                    onAddExpense = { dialogCategory = it }
                )
            }

            if (pendingExpenses.isNotEmpty()) {
                item {
                    PendingExpensesSection(
                        pending = pendingExpenses,
                        onCategorize = { expense, category -> viewModel.categorizePending(expense, category) },
                        onDiscard = { viewModel.discardPending(it) }
                    )
                }
            }
        }
    }

    dialogCategory?.let { category ->
        AddExpenseDialog(
            category = category,
            onDismiss = { dialogCategory = null },
            onConfirm = { amount, description ->
                viewModel.addManualExpense(category, amount, description)
                dialogCategory = null
            }
        )
    }
}
