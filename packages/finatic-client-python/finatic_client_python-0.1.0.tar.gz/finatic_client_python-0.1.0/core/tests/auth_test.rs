use finatic_client_core::auth::{AuthManager, TokenInfo};
use finatic_client_core::error::FinaticError;
use std::sync::Arc;
use tokio::sync::RwLock;

#[tokio::test]
async fn test_get_init_token() {
    let auth = AuthManager::new("test-api-key".to_string());
    let result = auth.get_init_token().await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_refresh_token() {
    let auth = AuthManager::new("test-api-key".to_string());
    let token = TokenInfo {
        access_token: "test-access-token".to_string(),
        refresh_token: "test-refresh-token".to_string(),
        expires_at: chrono::Utc::now() + chrono::Duration::minutes(5),
    };
    auth.set_token(Some(token));
    
    let result = auth.refresh_token().await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_revoke_token() {
    let auth = AuthManager::new("test-api-key".to_string());
    let token = TokenInfo {
        access_token: "test-access-token".to_string(),
        refresh_token: "test-refresh-token".to_string(),
        expires_at: chrono::Utc::now() + chrono::Duration::minutes(5),
    };
    auth.set_token(Some(token));
    
    let result = auth.revoke_token().await;
    assert!(result.is_ok());
    assert!(auth.get_token().await.is_none());
}

#[tokio::test]
async fn test_get_valid_token() {
    let auth = AuthManager::new("test-api-key".to_string());
    let token = TokenInfo {
        access_token: "test-access-token".to_string(),
        refresh_token: "test-refresh-token".to_string(),
        expires_at: chrono::Utc::now() + chrono::Duration::minutes(5),
    };
    auth.set_token(Some(token));
    
    let result = auth.get_valid_token().await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_token_expiration() {
    let auth = AuthManager::new("test-api-key".to_string());
    let token = TokenInfo {
        access_token: "test-access-token".to_string(),
        refresh_token: "test-refresh-token".to_string(),
        expires_at: chrono::Utc::now() - chrono::Duration::minutes(5),
    };
    auth.set_token(Some(token));
    
    let result = auth.get_valid_token().await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_invalid_api_key() {
    let auth = AuthManager::new("invalid-api-key".to_string());
    let result = auth.get_init_token().await;
    assert!(matches!(result, Err(FinaticError::AuthenticationError(_))));
} 