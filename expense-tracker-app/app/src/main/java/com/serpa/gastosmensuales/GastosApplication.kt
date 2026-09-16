package com.serpa.gastosmensuales

import android.app.Application
import com.serpa.gastosmensuales.data.AppDatabase
import com.serpa.gastosmensuales.data.ExpenseRepository

class GastosApplication : Application() {

    lateinit var repository: ExpenseRepository
        private set

    override fun onCreate() {
        super.onCreate()
        repository = ExpenseRepository(AppDatabase.getInstance(this))
    }
}
