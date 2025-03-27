use finatic_core::api::ApiClient;
use finatic_core::error::Error;
use finatic_core::auth::AuthManager;

#[tokio::test]
async fn test_security_api_key_validation() {
    // Test empty API key
    assert!(matches!(
        ApiClient::new("").get_user_data().await,
        Err(Error::AuthenticationError(_))
    ));
    
    // Test API key with invalid characters
    assert!(matches!(
        ApiClient::new("invalid/key!").get_user_data().await,
        Err(Error::AuthenticationError(_))
    ));
}

#[tokio::test]
async fn test_security_token_handling() {
    let auth = AuthManager::new("test_key");
    
    // Test token expiration
    let token = "expired_token";
    assert!(matches!(
        auth.validate_token(token).await,
        Err(Error::AuthenticationError(_))
    ));
    
    // Test token revocation
    assert!(matches!(
        auth.revoke_token().await,
        Ok(_) | Err(Error::AuthenticationError(_))
    ));
}

#[tokio::test]
async fn test_security_rate_limiting() {
    let client = ApiClient::new("test_key");
    
    // Test rate limiting with rapid requests
    for _ in 0..100 {
        let result = client.get_user_data().await;
        if let Err(Error::RateLimitExceeded(_)) = result {
            return; // Test passed if we hit rate limit
        }
    }
    panic!("Rate limiting not working as expected");
}

#[tokio::test]
async fn test_security_input_validation() {
    let client = ApiClient::new("test_key");
    
    // Test SQL injection attempt
    assert!(matches!(
        client.get_user_data_with_query("'; DROP TABLE users; --").await,
        Err(Error::ValidationError(_))
    ));
    
    // Test XSS attempt
    assert!(matches!(
        client.get_user_data_with_query("<script>alert('xss')</script>").await,
        Err(Error::ValidationError(_))
    ));
} 