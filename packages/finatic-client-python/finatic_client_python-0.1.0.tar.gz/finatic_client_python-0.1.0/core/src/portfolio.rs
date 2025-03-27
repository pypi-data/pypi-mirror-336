use async_trait::async_trait;
use tracing::{debug, info};

use crate::{Result, api::ApiClient, models::{Portfolio, Performance}};

#[cfg(feature = "python")]
use pyo3::prelude::*;

#[async_trait]
pub trait PortfolioService: Send + Sync {
    async fn get_portfolio(&self) -> Result<Portfolio>;
    async fn get_performance(&self) -> Result<Performance>;
}

#[cfg_attr(feature = "python", pyclass)]
#[derive(Debug)]
pub struct PortfolioClient {
    api: ApiClient,
}

impl PortfolioClient {
    pub fn new(api: ApiClient) -> Self {
        Self { api }
    }

    pub async fn get_portfolio(&self) -> Result<Portfolio> {
        self.api.get("/portfolio").await
    }

    pub async fn get_performance(&self) -> Result<Performance> {
        self.api.get("/portfolio/performance").await
    }
}

#[cfg(feature = "python")]
#[pymethods]
impl PortfolioClient {
    #[new]
    fn py_new(api: ApiClient) -> Self {
        Self::new(api)
    }

    fn py_get_portfolio(&self) -> PyResult<Portfolio> {
        let rt = tokio::runtime::Runtime::new()?;
        rt.block_on(self.get_portfolio())
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }

    fn py_get_performance(&self) -> PyResult<Performance> {
        let rt = tokio::runtime::Runtime::new()?;
        rt.block_on(self.get_performance())
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }
}

pub struct FinaticPortfolioService {
    client: ApiClient,
}

impl FinaticPortfolioService {
    pub fn new(client: ApiClient) -> Self {
        Self { client }
    }
}

#[async_trait]
impl PortfolioService for FinaticPortfolioService {
    async fn get_portfolio(&self) -> Result<Portfolio> {
        debug!("Fetching portfolio");
        let portfolio: Portfolio = self.client.get("/portfolio").await?;
        info!("Retrieved portfolio with {} positions", portfolio.positions.len());
        Ok(portfolio)
    }

    async fn get_performance(&self) -> Result<Performance> {
        debug!("Fetching performance");
        let performance: Performance = self.client.get("/portfolio/performance").await?;
        info!("Retrieved performance data");
        Ok(performance)
    }
} 