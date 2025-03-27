use finatic_client_core::api::ApiClient;
use finatic_client_core::error::FinaticError;
use finatic_client_core::models::{Holding, Portfolio, Order};

#[tokio::test]
async fn test_get_holdings() {
    let client = ApiClient::new("test-api-key".to_string());
    let result = client.get_holdings().await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_get_portfolio() {
    let client = ApiClient::new("test-api-key".to_string());
    let result = client.get_portfolio().await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_place_order() {
    let client = ApiClient::new("test-api-key".to_string());
    let order = Order {
        symbol: "AAPL".to_string(),
        side: "buy".to_string(),
        quantity: 10,
        order_type: "market".to_string(),
        time_in_force: "day".to_string(),
        limit_price: None,
        stop_price: None,
    };
    let result = client.place_order(order).await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_invalid_api_key() {
    let client = ApiClient::new("invalid-api-key".to_string());
    let result = client.get_holdings().await;
    assert!(matches!(result, Err(FinaticError::AuthenticationError(_))));
}

#[tokio::test]
async fn test_rate_limiting() {
    let client = ApiClient::new("test-api-key".to_string());
    let mut results = Vec::new();
    for _ in 0..100 {
        results.push(client.get_holdings().await);
    }
    assert!(results.iter().any(|r| matches!(r, Err(FinaticError::RateLimitError(_)))));
} 