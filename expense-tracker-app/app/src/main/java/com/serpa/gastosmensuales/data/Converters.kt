package com.serpa.gastosmensuales.data

import androidx.room.TypeConverter

class Converters {
    @TypeConverter
    fun fromCategory(category: Category?): String? = category?.name

    @TypeConverter
    fun toCategory(value: String?): Category? = value?.let { Category.valueOf(it) }

    @TypeConverter
    fun fromSource(source: ExpenseSource): String = source.name

    @TypeConverter
    fun toSource(value: String): ExpenseSource = ExpenseSource.valueOf(value)
}
