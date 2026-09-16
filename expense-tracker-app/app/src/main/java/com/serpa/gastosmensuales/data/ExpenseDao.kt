package com.serpa.gastosmensuales.data

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Update
import kotlinx.coroutines.flow.Flow

@Dao
interface ExpenseDao {

    @Insert
    suspend fun insert(expense: Expense): Long

    @Update
    suspend fun update(expense: Expense)

    @Delete
    suspend fun delete(expense: Expense)

    @Query("SELECT * FROM expenses WHERE yearMonth = :yearMonth ORDER BY timestampMillis DESC")
    fun expensesForMonth(yearMonth: String): Flow<List<Expense>>

    @Query("SELECT * FROM expenses WHERE category IS NULL ORDER BY timestampMillis DESC")
    fun uncategorizedExpenses(): Flow<List<Expense>>

    @Query(
        "SELECT category, SUM(amount) as total FROM expenses " +
            "WHERE yearMonth = :yearMonth AND category IS NOT NULL GROUP BY category"
    )
    fun totalsByCategory(yearMonth: String): Flow<List<CategoryTotal>>
}
