use pyo3::prelude::*;
use finatic_core::ApiClient;
use tokio::runtime::Runtime;

#[pymodule]
fn _core(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Client>()?;
    Ok(())
}

#[pyclass]
struct Client {
    inner: ApiClient,
    runtime: Runtime,
}

#[pymethods]
impl Client {
    #[new]
    fn new(api_key: String, base_url: String) -> PyResult<Self> {
        let runtime = Runtime::new().map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;
        Ok(Self {
            inner: ApiClient::new(api_key.to_string(), base_url.to_string()),
            runtime,
        })
    }

    fn get_user_token(&self, user_id: String) -> PyResult<String> {
        let inner = &self.inner;
        let user_id = user_id.clone();
        let token = self.runtime.block_on(async move {
            inner.get_user_token(&user_id).await
        }).map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;
        Ok(token.access_token)
    }

    fn health_check(&self) -> PyResult<bool> {
        let inner = &self.inner;
        self.runtime.block_on(async move {
            inner.health_check().await
        }).map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }
} 