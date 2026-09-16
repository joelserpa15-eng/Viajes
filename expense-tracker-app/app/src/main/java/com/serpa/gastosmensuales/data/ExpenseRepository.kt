package com.serpa.gastosmensuales.data

import java.time.YearMonth

fun currentYearMonth(): String = YearMonth.now().toString()

class ExpenseRepository(db: AppDatabase) {
    private val expenseDao = db.expenseDao()
    private val budgetDao = db.budgetDao()

    fun expensesForMonth(yearMonth: String) = expenseDao.expensesForMonth(yearMonth)

    fun uncategorizedExpenses() = expenseDao.uncategorizedExpenses()

    fun totalsByCategory(yearMonth: String) = expenseDao.totalsByCategory(yearMonth)

    fun observeBudget(yearMonth: String) = budgetDao.observeBudget(yearMonth)

    suspend fun addExpense(
        amount: Double,
        category: Category?,
        description: String,
        source: ExpenseSource,
        yearMonth: String = currentYearMonth()
    ) {
        expenseDao.insert(
            Expense(
                amount = amount,
                category = category,
                description = description,
                source = source,
                timestampMillis = System.currentTimeMillis(),
                yearMonth = yearMonth
            )
        )
    }

    suspend fun categorize(expense: Expense, category: Category) {
        expenseDao.update(expense.copy(category = category))
    }

    suspend fun deleteExpense(expense: Expense) {
        expenseDao.delete(expense)
    }

    suspend fun saveBudget(budget: MonthlyBudget) {
        budgetDao.upsert(budget)
    }
}
