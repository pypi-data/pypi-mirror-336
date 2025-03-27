use async_trait::async_trait;
use tracing::{debug, info};

use crate::{Error, Result, api::ApiClient, models::{Account, Holding, Order, OrderStatus}};

#[cfg(feature = "python")]
use pyo3::prelude::*;

#[async_trait]
pub trait TradingService: Send + Sync {
    async fn get_accounts(&self) -> Result<Vec<Account>>;
    async fn get_holdings(&self) -> Result<Vec<Holding>>;
    async fn place_order(&self, order: &Order) -> Result<String>;
}

pub struct FinaticTradingService {
    client: ApiClient,
}

impl FinaticTradingService {
    pub fn new(client: ApiClient) -> Self {
        Self { client }
    }
}

#[async_trait]
impl TradingService for FinaticTradingService {
    async fn get_accounts(&self) -> Result<Vec<Account>> {
        debug!("Fetching accounts");
        let accounts: Vec<Account> = self.client.get("/accounts").await?;
        info!("Retrieved {} accounts", accounts.len());
        Ok(accounts)
    }

    async fn get_holdings(&self) -> Result<Vec<Holding>> {
        debug!("Fetching holdings");
        let holdings: Vec<Holding> = self.client.get("/holdings").await?;
        info!("Retrieved {} holdings", holdings.len());
        Ok(holdings)
    }

    async fn place_order(&self, order: &Order) -> Result<String> {
        debug!("Placing order: {:?}", order);
        let response: serde_json::Value = self.client.post("/trading/orders", Some(order)).await?;
        let order_id = response.get("order_id")
            .and_then(|v| v.as_str())
            .ok_or_else(|| Error::InvalidResponse("Missing order_id in response".to_string()))?;
        info!("Order placed successfully: {}", order_id);
        Ok(order_id.to_string())
    }
}

#[cfg_attr(feature = "python", pyclass)]
#[derive(Debug)]
pub struct TradingClient {
    api: ApiClient,
}

impl TradingClient {
    pub fn new(api: ApiClient) -> Self {
        Self { api }
    }

    pub async fn place_order(&self, order: Order) -> Result<String> {
        let service = FinaticTradingService::new(self.api.clone());
        service.place_order(&order).await
    }

    pub async fn get_order_status(&self, order_id: &str) -> Result<OrderStatus> {
        self.api.get(&format!("/trading/orders/{}", order_id)).await
    }

    pub async fn cancel_order(&self, order_id: &str) -> Result<()> {
        self.api.post(&format!("/trading/orders/{}/cancel", order_id), None::<()>).await
    }
}

#[cfg(feature = "python")]
#[pymethods]
impl TradingClient {
    #[new]
    fn py_new(api: ApiClient) -> Self {
        Self::new(api)
    }

    fn py_place_order(&self, order: Order) -> PyResult<String> {
        let rt = tokio::runtime::Runtime::new()?;
        rt.block_on(self.place_order(order))
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }

    fn py_get_order_status(&self, order_id: &str) -> PyResult<OrderStatus> {
        let rt = tokio::runtime::Runtime::new()?;
        rt.block_on(self.get_order_status(order_id))
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }

    fn py_cancel_order(&self, order_id: &str) -> PyResult<()> {
        let rt = tokio::runtime::Runtime::new()?;
        rt.block_on(self.cancel_order(order_id))
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }
} 