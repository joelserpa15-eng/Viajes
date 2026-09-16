package com.serpa.gastosmensuales

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.lifecycle.viewmodel.compose.viewModel
import com.serpa.gastosmensuales.ui.AppRoot
import com.serpa.gastosmensuales.ui.theme.GastosMensualesTheme
import com.serpa.gastosmensuales.viewmodel.ExpenseViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val repository = (application as GastosApplication).repository

        setContent {
            GastosMensualesTheme {
                val viewModel: ExpenseViewModel = viewModel(factory = ExpenseViewModel.factory(repository))
                AppRoot(viewModel = viewModel)
            }
        }
    }
}
