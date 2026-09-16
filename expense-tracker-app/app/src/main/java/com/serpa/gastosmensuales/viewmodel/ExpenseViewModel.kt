package com.serpa.gastosmensuales.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import com.serpa.gastosmensuales.data.Category
import com.serpa.gastosmensuales.data.Expense
import com.serpa.gastosmensuales.data.ExpenseRepository
import com.serpa.gastosmensuales.data.ExpenseSource
import com.serpa.gastosmensuales.data.MonthlyBudget
import com.serpa.gastosmensuales.data.currentYearMonth
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class ExpenseViewModel(private val repository: ExpenseRepository) : ViewModel() {

    private val yearMonth: String = currentYearMonth()

    val budget: StateFlow<MonthlyBudget?> =
        repository.observeBudget(yearMonth)
            .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), null)

    val categoryTotals: StateFlow<Map<Category, Double>> =
        repository.totalsByCategory(yearMonth)
            .map { totals -> totals.associate { it.category to it.total } }
            .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyMap())

    val pendingExpenses: StateFlow<List<Expense>> =
        repository.uncategorizedExpenses()
            .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())

    fun currentMonth(): String = yearMonth

    fun saveBudget(income: Double, savingsPercent: Double, basicPercent: Double, personalPercent: Double) {
        viewModelScope.launch {
            repository.saveBudget(
                MonthlyBudget(
                    yearMonth = yearMonth,
                    income = income,
                    savingsPercent = savingsPercent,
                    basicPercent = basicPercent,
                    personalPercent = personalPercent
                )
            )
        }
    }

    fun addManualExpense(category: Category, amount: Double, description: String) {
        viewModelScope.launch {
            repository.addExpense(
                amount = amount,
                category = category,
                description = description,
                source = ExpenseSource.MANUAL,
                yearMonth = yearMonth
            )
        }
    }

    fun categorizePending(expense: Expense, category: Category) {
        viewModelScope.launch { repository.categorize(expense, category) }
    }

    fun discardPending(expense: Expense) {
        viewModelScope.launch { repository.deleteExpense(expense) }
    }

    companion object {
        fun factory(repository: ExpenseRepository) = viewModelFactory {
            initializer { ExpenseViewModel(repository) }
        }
    }
}
