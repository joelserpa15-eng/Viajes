package com.serpa.gastosmensuales.ui

import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import com.serpa.gastosmensuales.viewmodel.ExpenseViewModel

@Composable
fun AppRoot(viewModel: ExpenseViewModel) {
    val budget by viewModel.budget.collectAsState()
    var editingBudget by remember { mutableStateOf(false) }

    if (budget == null || editingBudget) {
        BudgetSetupScreen(
            existing = budget,
            onSave = { income, savings, basic, personal ->
                viewModel.saveBudget(income, savings, basic, personal)
                editingBudget = false
            },
            onCancel = if (budget != null) {
                { editingBudget = false }
            } else {
                null
            }
        )
    } else {
        DashboardScreen(
            viewModel = viewModel,
            budget = budget!!,
            onEditBudget = { editingBudget = true }
        )
    }
}
