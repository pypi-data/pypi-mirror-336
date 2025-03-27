use finatic_core::api::ApiClient;
use finatic_core::error::Error;
use finatic_core::models::*;
use wiremock::{Mock, MockServer, ResponseTemplate};

#[tokio::test]
async fn test_integration_user_data() {
    let mock_server = MockServer::start().await;
    
    Mock::given(wiremock::matchers::path("/api/v1/user"))
        .respond_with(ResponseTemplate::new(200)
            .set_body_json(json!({
                "id": "user123",
                "email": "test@example.com",
                "name": "Test User"
            })))
        .expect(1)
        .mount(&mock_server)
        .await;

    let client = ApiClient::new_with_base_url("test_key", &mock_server.uri());
    let result = client.get_user_data().await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_integration_portfolio() {
    let mock_server = MockServer::start().await;
    
    Mock::given(wiremock::matchers::path("/api/v1/portfolio"))
        .respond_with(ResponseTemplate::new(200)
            .set_body_json(json!({
                "total_value": 10000.0,
                "positions": [
                    {
                        "symbol": "AAPL",
                        "quantity": 10,
                        "average_price": 150.0
                    }
                ]
            })))
        .expect(1)
        .mount(&mock_server)
        .await;

    let client = ApiClient::new_with_base_url("test_key", &mock_server.uri());
    let result = client.get_portfolio().await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_integration_trading() {
    let mock_server = MockServer::start().await;
    
    Mock::given(wiremock::matchers::path("/api/v1/orders"))
        .respond_with(ResponseTemplate::new(200)
            .set_body_json(json!({
                "id": "order123",
                "status": "filled",
                "symbol": "AAPL",
                "side": "buy",
                "quantity": 1,
                "price": 150.0
            })))
        .expect(1)
        .mount(&mock_server)
        .await;

    let client = ApiClient::new_with_base_url("test_key", &mock_server.uri());
    let order = OrderRequest {
        symbol: "AAPL".to_string(),
        side: OrderSide::Buy,
        quantity: 1,
        order_type: OrderType::Market,
        price: None,
        time_in_force: None,
    };
    let result = client.place_order(order).await;
    assert!(result.is_ok());
} 