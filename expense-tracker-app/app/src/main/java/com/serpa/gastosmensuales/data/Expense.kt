package com.serpa.gastosmensuales.data

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Un gasto individual. [category] es null cuando el gasto proviene de una notificación
 * de Google Pay detectada automáticamente y todavía no se ha asignado a una clasificación.
 */
@Entity(tableName = "expenses")
data class Expense(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val amount: Double,
    val category: Category?,
    val description: String,
    val source: ExpenseSource,
    val timestampMillis: Long,
    val yearMonth: String
)

/** Resultado de agregación: total gastado por clasificación en un mes. */
data class CategoryTotal(
    val category: Category,
    val total: Double
)
