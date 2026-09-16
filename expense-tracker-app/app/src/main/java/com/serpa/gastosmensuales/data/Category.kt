package com.serpa.gastosmensuales.data

/** Las tres clasificaciones de gasto que el usuario configura cada mes. */
enum class Category(val displayName: String) {
    SAVINGS("Ahorro"),
    BASIC("Gastos básicos"),
    PERSONAL("Gastos personales")
}

/** Origen de un registro de gasto. */
enum class ExpenseSource {
    MANUAL,
    GOOGLE_PAY
}
