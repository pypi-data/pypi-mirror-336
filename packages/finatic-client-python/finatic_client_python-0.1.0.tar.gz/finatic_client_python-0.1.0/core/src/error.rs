use thiserror::Error;
#[cfg(feature = "python")]
use pyo3::prelude::*;

#[derive(Error, Debug)]
pub enum Error {
    #[error("Request failed: {0}")]
    RequestFailed(String),

    #[error("API error {0}: {1}")]
    ApiError(u16, String),

    #[error("Deserialization failed: {0}")]
    DeserializationFailed(String),

    #[error("Authentication failed: {0}")]
    Auth(String),

    #[error("Token expired")]
    TokenExpired,

    #[error("Invalid configuration: {0}")]
    InvalidConfig(String),

    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),

    #[error("Serialization error: {0}")]
    SerializationError(#[from] serde_json::Error),

    #[error("Invalid response: {0}")]
    InvalidResponse(String),
}

impl From<reqwest::Error> for Error {
    fn from(err: reqwest::Error) -> Self {
        if err.is_timeout() {
            Error::RequestFailed("Request timed out".to_string())
        } else if err.is_connect() {
            Error::RequestFailed("Failed to connect".to_string())
        } else {
            Error::RequestFailed(err.to_string())
        }
    }
}

#[cfg(feature = "python")]
impl From<Error> for PyErr {
    fn from(err: Error) -> PyErr {
        match err {
            Error::RequestFailed(msg) => PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(msg),
            Error::ApiError(status, msg) => PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("API error {}: {}", status, msg)),
            Error::DeserializationFailed(msg) => PyErr::new::<pyo3::exceptions::PyValueError, _>(msg),
            Error::Auth(msg) => PyErr::new::<pyo3::exceptions::PyPermissionError, _>(msg),
            Error::TokenExpired => PyErr::new::<pyo3::exceptions::PyPermissionError, _>("Token expired"),
            Error::InvalidConfig(msg) => PyErr::new::<pyo3::exceptions::PyValueError, _>(msg),
            Error::IoError(err) => PyErr::new::<pyo3::exceptions::PyIOError, _>(err.to_string()),
            Error::SerializationError(err) => PyErr::new::<pyo3::exceptions::PyValueError, _>(err.to_string()),
            Error::InvalidResponse(msg) => PyErr::new::<pyo3::exceptions::PyValueError, _>(msg),
        }
    }
}