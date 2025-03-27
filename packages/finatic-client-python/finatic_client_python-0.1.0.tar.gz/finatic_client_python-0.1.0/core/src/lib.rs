//! Finatic Backend SDK
//! 
//! This crate provides a secure and efficient SDK for integrating with the Finatic platform.
//! 
//! # Examples
//! 
//! ```no_run
//! use finatic_client_core::ApiClient;
//! 
//! #[tokio::main]
//! async fn main() -> Result<(), Box<dyn std::error::Error>> {
//!     let client = ApiClient::new("your_api_key", "https://api.finatic.dev");
//!     
//!     // Get portfolio
//!     let portfolio = client.get("/portfolio").await?;
//!     println!("Portfolio: {:?}", portfolio);
//!     
//!     // Place an order
//!     let order = Order {
//!         symbol: "AAPL".to_string(),
//!         side: OrderSide::Buy,
//!         quantity: 1.0,
//!         order_type: OrderType::Market,
//!         price: None,
//!         time_in_force: None,
//!     };
//!     let order_id = client.post("/orders", Some(order)).await?;
//!     println!("Order ID: {:?}", order_id);
//!     
//!     Ok(())
//! }
//! ```
//! 
//! # Features
//! 
//! - Secure API key management
//! - Automatic token refresh
//! - Rate limiting and retry logic
//! - Comprehensive error handling
//! - Async/await support
//! - Type-safe API
//! 
//! # Error Handling
//! 
//! The SDK uses custom error types for different failure scenarios:
//! 
//! ```no_run
//! use finatic_client_core::Error;
//! 
//! match client.get("/user").await {
//!     Ok(data) => println!("Success: {:?}", data),
//!     Err(Error::AuthenticationFailed(e)) => println!("Auth error: {}", e),
//!     Err(Error::RequestFailed(e)) => println!("Request failed: {}", e),
//!     Err(Error::ApiError(status, msg)) => println!("API error {}: {}", status, msg),
//!     Err(e) => println!("Other error: {}", e),
//! }
//! ```

pub mod api;
pub mod auth;
pub mod error;
pub mod models;
pub mod trading;
pub mod portfolio;
pub mod analytics;

// Re-export commonly used types
pub use api::ApiClient;
pub use auth::AuthManager;
pub use error::Error;
pub use models::*;
pub use trading::TradingClient;
pub use portfolio::PortfolioClient;
pub use analytics::AnalyticsClient;

// Re-export Result type
pub type Result<T> = std::result::Result<T, Error>;

#[cfg(feature = "python")]
use pyo3::prelude::*;

#[cfg(feature = "python")]
#[pymodule]
fn _core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<ApiClient>()?;
    m.add_class::<TradingClient>()?;
    m.add_class::<PortfolioClient>()?;
    m.add_class::<AnalyticsClient>()?;
    Ok(())
} 