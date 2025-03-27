use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::exceptions::PyValueError;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

use crate::{
    api::ApiClient,
    models::{Account, Holding, Order, Portfolio, Performance, Event},
    trading::FinaticTradingService,
    portfolio::FinaticPortfolioService,
    analytics::FinaticAnalyticsService,
};

#[pyclass]
pub struct FinaticClient {
    trading: FinaticTradingService,
    portfolio: FinaticPortfolioService,
    analytics: FinaticAnalyticsService,
}

#[pymethods]
impl FinaticClient {
    #[new]
    pub fn new(api_key: String, base_url: String) -> Self {
        let client = ApiClient::new(base_url.clone(), api_key);
        Self {
            trading: FinaticTradingService::new(client.clone()),
            portfolio: FinaticPortfolioService::new(client.clone()),
            analytics: FinaticAnalyticsService::new(client),
        }
    }

    pub async fn get_accounts(&self) -> PyResult<Vec<Account>> {
        self.trading.get_accounts().await.map_err(|e| {
            PyValueError::new_err(format!("Failed to get accounts: {}", e))
        })
    }

    pub async fn get_holdings(&self) -> PyResult<Vec<Holding>> {
        self.trading.get_holdings().await.map_err(|e| {
            PyValueError::new_err(format!("Failed to get holdings: {}", e))
        })
    }

    pub async fn place_order(&self, order: Order) -> PyResult<String> {
        self.trading.place_order(&order).await.map_err(|e| {
            PyValueError::new_err(format!("Failed to place order: {}", e))
        })
    }

    pub async fn get_portfolio(&self) -> PyResult<Portfolio> {
        self.portfolio.get_portfolio().await.map_err(|e| {
            PyValueError::new_err(format!("Failed to get portfolio: {}", e))
        })
    }

    pub async fn get_performance(&self) -> PyResult<Performance> {
        self.portfolio.get_performance().await.map_err(|e| {
            PyValueError::new_err(format!("Failed to get performance: {}", e))
        })
    }

    pub async fn get_analytics(
        &self,
        metrics: Vec<String>,
        start_date: Option<String>,
        end_date: Option<String>,
        group_by: Option<String>,
    ) -> PyResult<&PyDict> {
        let request = crate::analytics::AnalyticsRequest {
            start_date,
            end_date,
            metrics,
            group_by,
        };

        let analytics = self.analytics.get_analytics(&request).await.map_err(|e| {
            PyValueError::new_err(format!("Failed to get analytics: {}", e))
        })?;

        let dict = PyDict::new(py);
        for (key, value) in analytics.as_object().unwrap() {
            dict.set_item(key, value)?;
        }

        Ok(dict)
    }

    pub async fn get_events(&self, event_type: Option<String>) -> PyResult<Vec<Event>> {
        self.analytics.get_events(event_type.as_deref()).await.map_err(|e| {
            PyValueError::new_err(format!("Failed to get events: {}", e))
        })
    }
}

#[pymodule]
fn _core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<FinaticClient>()?;
    Ok(())
} 