package com.serpa.gastosmensuales.data

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Presupuesto configurado por el usuario para un mes concreto ("2026-09").
 * Los tres porcentajes deben sumar 100.
 */
@Entity(tableName = "monthly_budgets")
data class MonthlyBudget(
    @PrimaryKey val yearMonth: String,
    val income: Double,
    val savingsPercent: Double,
    val basicPercent: Double,
    val personalPercent: Double
) {
    fun percentFor(category: Category): Double = when (category) {
        Category.SAVINGS -> savingsPercent
        Category.BASIC -> basicPercent
        Category.PERSONAL -> personalPercent
    }

    fun limitFor(category: Category): Double = income * percentFor(category) / 100.0
}
