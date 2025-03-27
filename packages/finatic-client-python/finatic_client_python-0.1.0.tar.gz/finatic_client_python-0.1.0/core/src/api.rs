use reqwest::Client;
use std::sync::Arc;
use serde_json::Value;
use tokio::runtime::Runtime;

use pyo3::{
    prelude::*,
    types::{PyBool, PyDict, PyList},
    exceptions::{PyValueError, PyRuntimeError},
};

use crate::{Error, Result, auth::AuthManager, models::{PortalResponse, UserToken}};

use reqwest::{Method};
use std::time::Duration;
use std::collections::HashMap;
use tokio::sync::RwLock;

#[cfg(feature = "python")]
trait ToPyObject {
    fn to_py_object(&self, py: Python) -> PyResult<PyObject>;
}

#[cfg(feature = "python")]
impl ToPyObject for serde_json::Value {
    fn to_py_object(&self, py: Python) -> PyResult<PyObject> {
        match self {
            serde_json::Value::Null => Ok(py.None().into()),
            serde_json::Value::Bool(b) => Ok(PyBool::new(py, *b).into()),
            serde_json::Value::Number(n) => {
                if let Some(i) = n.as_i64() {
                    Ok(i.into_py(py))
                } else if let Some(f) = n.as_f64() {
                    Ok(f.into_py(py))
                } else {
                    Err(PyValueError::new_err("Invalid number"))
                }
            }
            serde_json::Value::String(s) => Ok(s.into_py(py)),
            serde_json::Value::Array(arr) => {
                let py_list = PyList::new(py, &[]);
                for value in arr {
                    let py_value = value.to_py_object(py)?;
                    py_list.append(py_value)?;
                }
                Ok(py_list.into())
            }
            serde_json::Value::Object(obj) => {
                let py_dict = PyDict::new(py);
                for (key, value) in obj {
                    let py_value = value.to_py_object(py)?;
                    py_dict.set_item(key, py_value)?;
                }
                Ok(py_dict.into())
            }
        }
    }
}

#[cfg_attr(feature = "python", pyclass)]
#[derive(Debug, Clone)]
pub struct ApiClient {
    client: Client,
    auth: Arc<AuthManager>,
    base_url: String,
}

impl ApiClient {
    pub fn new(api_key: String, base_url: String) -> Self {
        let auth = AuthManager::new(api_key.clone(), base_url.clone());
        Self {
            client: Client::new(),
            auth: Arc::new(auth),
            base_url,
        }
    }

    pub async fn get<T: for<'de> serde::Deserialize<'de>>(&self, path: &str) -> Result<T> {
        let token = self.auth.get_valid_token().await?;
        let response = self.client
            .get(format!("{}{}", self.base_url, path))
            .header("Authorization", format!("Bearer {}", token))
            .send()
            .await?;

        if !response.status().is_success() {
            return Err(Error::ApiError(
                response.status().as_u16(),
                response.text().await.unwrap_or_default(),
            ));
        }

        let data: T = response.json().await?;
        Ok(data)
    }

    pub async fn post<T: for<'de> serde::Deserialize<'de>, B: serde::Serialize>(
        &self,
        path: &str,
        body: Option<B>,
    ) -> Result<T> {
        let token = self.auth.get_valid_token().await?;
        let mut request = self.client
            .post(format!("{}{}", self.base_url, path))
            .header("Authorization", format!("Bearer {}", token));

        if let Some(body) = body {
            request = request.json(&body);
        }

        let response = request.send().await?;

        if !response.status().is_success() {
            return Err(Error::ApiError(
                response.status().as_u16(),
                response.text().await.unwrap_or_default(),
            ));
        }

        let data: T = response.json().await?;
        Ok(data)
    }

    pub async fn health_check(&self) -> Result<bool> {
        let response = self.get::<serde_json::Value>("/health").await?;
        Ok(response.get("status").and_then(|v| v.as_str()) == Some("ok"))
    }

    pub async fn generate_portal_token(&self) -> Result<PortalResponse> {
        self.post("/portal/token", None::<()>).await
    }

    pub async fn get_user_token(&self, user_id: &str) -> Result<UserToken> {
        self.get(&format!("/users/{}/token", user_id)).await
    }

    pub async fn refresh_user_token(&self, user_id: &str) -> Result<UserToken> {
        self.post(&format!("/users/{}/token/refresh", user_id), None::<()>).await
    }

    pub async fn revoke_user_access(&self, user_id: &str) -> Result<()> {
        self.post(&format!("/users/{}/token/revoke", user_id), None::<()>).await
    }
}

#[cfg(feature = "python")]
#[pymethods]
impl ApiClient {
    #[new]
    fn py_new(api_key: String, base_url: String) -> Self {
        Self::new(api_key, base_url)
    }

    fn py_get(&self, path: &str) -> PyResult<PyObject> {
        let rt = tokio::runtime::Runtime::new()?;
        let response: serde_json::Value = rt.block_on(self.get(path))
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;
        
        Python::with_gil(|py| response.to_py_object(py))
    }

    fn py_post(&self, path: &str, body: Option<serde_json::Value>) -> PyResult<PyObject> {
        let rt = tokio::runtime::Runtime::new()?;
        let response: serde_json::Value = rt.block_on(self.post(path, body))
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;
        
        Python::with_gil(|py| response.to_py_object(py))
    }

    fn py_health_check(&self) -> PyResult<bool> {
        let rt = tokio::runtime::Runtime::new()?;
        rt.block_on(self.health_check())
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }

    fn py_generate_portal_token(&self) -> PyResult<PortalResponse> {
        let rt = tokio::runtime::Runtime::new()?;
        rt.block_on(self.generate_portal_token())
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }

    fn py_get_user_token(&self, user_id: &str) -> PyResult<UserToken> {
        let rt = tokio::runtime::Runtime::new()?;
        rt.block_on(self.get_user_token(user_id))
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }

    fn py_refresh_user_token(&self, user_id: &str) -> PyResult<UserToken> {
        let rt = tokio::runtime::Runtime::new()?;
        rt.block_on(self.refresh_user_token(user_id))
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }

    fn py_revoke_user_access(&self, user_id: &str) -> PyResult<()> {
        let rt = tokio::runtime::Runtime::new()?;
        rt.block_on(self.revoke_user_access(user_id))
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
    }
} 