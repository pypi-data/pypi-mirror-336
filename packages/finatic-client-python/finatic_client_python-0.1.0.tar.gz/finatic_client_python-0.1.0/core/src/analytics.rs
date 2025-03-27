use async_trait::async_trait;
use tracing::{debug, info};
use serde::Serialize;

use crate::{Result, api::ApiClient, models::Event};

#[cfg(feature = "python")]
use pyo3::prelude::*;

#[cfg_attr(feature = "python", pyclass)]
#[derive(Debug, Serialize)]
pub struct AnalyticsRequest {
    pub start_date: Option<String>,
    pub end_date: Option<String>,
    pub metrics: Vec<String>,
    pub group_by: Option<String>,
}

#[async_trait]
pub trait AnalyticsService: Send + Sync {
    async fn get_analytics(&self, request: &AnalyticsRequest) -> Result<serde_json::Value>;
    async fn get_events(&self, event_type: Option<&str>) -> Result<Vec<Event>>;
}

pub struct FinaticAnalyticsService {
    client: ApiClient,
}

impl FinaticAnalyticsService {
    pub fn new(client: ApiClient) -> Self {
        Self { client }
    }
}

#[async_trait]
impl AnalyticsService for FinaticAnalyticsService {
    async fn get_analytics(&self, request: &AnalyticsRequest) -> Result<serde_json::Value> {
        debug!("Fetching analytics with request: {:?}", request);
        let analytics: serde_json::Value = self.client.post("/analytics", Some(request)).await?;
        info!("Retrieved analytics data");
        Ok(analytics)
    }

    async fn get_events(&self, event_type: Option<&str>) -> Result<Vec<Event>> {
        let path = if let Some(typ) = event_type {
            format!("/events?type={}", typ)
        } else {
            "/events".to_string()
        };
        
        debug!("Fetching events{}", event_type.map(|t| format!(" of type: {}", t)).unwrap_or_default());
        let events: Vec<Event> = self.client.get(&path).await?;
        info!("Retrieved {} events", events.len());
        Ok(events)
    }
}

#[cfg_attr(feature = "python", pyclass)]
#[derive(Debug)]
pub struct AnalyticsClient {
    api: ApiClient,
}

impl AnalyticsClient {
    pub fn new(api: ApiClient) -> Self {
        Self { api }
    }

    pub async fn track_event(&self, event: Event) -> Result<()> {
        self.api.post("/events", Some(event)).await
    }

    pub async fn get_events(&self) -> Result<Vec<Event>> {
        self.api.get("/events").await
    }
}

#[cfg(feature = "python")]
#[pymethods]
impl AnalyticsClient {
    #[new]
    fn py_new(api: ApiClient) -> Self {
        Self::new(api)
    }

    fn py_track_event(&self, event: Event) -> PyResult<()> {
        let rt = tokio::runtime::Runtime::new()?;
        rt.block_on(self.track_event(event))
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }

    fn py_get_events(&self) -> PyResult<Vec<Event>> {
        let rt = tokio::runtime::Runtime::new()?;
        rt.block_on(self.get_events())
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }
} 