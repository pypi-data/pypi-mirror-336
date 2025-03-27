use std::sync::Arc;
use tokio::sync::RwLock;
use reqwest::Client;
use uuid::Uuid;
use std::time::Instant;

use crate::{Error, Result, models::{TokenResponse, UserToken, PortalResponse}};

#[derive(Debug, Clone)]
pub struct AuthManager {
    client: Client,
    api_key: String,
    base_url: String,
    token: Arc<RwLock<Option<TokenData>>>,
}

#[derive(Debug, Clone)]
struct TokenData {
    access_token: String,
    expires_at: Instant,
}

impl AuthManager {
    pub fn new(api_key: String, base_url: String) -> Self {
        Self {
            client: Client::new(),
            api_key,
            base_url,
            token: Arc::new(RwLock::new(None)),
        }
    }

    pub async fn generate_portal_token(&self) -> Result<PortalResponse> {
        let session_id = Uuid::new_v4().to_string();
        let response = self.client
            .post(format!("{}/auth/portal", self.base_url))
            .header("X-API-Key", &self.api_key)
            .json(&serde_json::json!({
                "company_id": self.api_key.split(':').next().unwrap_or_default(),
                "session_id": session_id,
            }))
            .send()
            .await?;

        if !response.status().is_success() {
            return Err(Error::Auth(format!(
                "Failed to generate portal token: {}",
                response.status()
            )));
        }

        let portal_response: PortalResponse = response.json().await?;
        Ok(portal_response)
    }

    pub async fn get_user_token(&self, user_id: &str) -> Result<UserToken> {
        let response = self.client
            .post(format!("{}/auth/user", self.base_url))
            .header("X-API-Key", &self.api_key)
            .json(&serde_json::json!({
                "user_id": user_id,
                "company_id": self.api_key.split(':').next().unwrap_or_default(),
            }))
            .send()
            .await?;

        if !response.status().is_success() {
            return Err(Error::Auth(format!(
                "Failed to get user token: {}",
                response.status()
            )));
        }

        let user_token: UserToken = response.json().await?;
        Ok(user_token)
    }

    pub async fn refresh_user_token(&self, user_id: &str) -> Result<UserToken> {
        let response = self.client
            .post(format!("{}/auth/user/refresh", self.base_url))
            .header("X-API-Key", &self.api_key)
            .json(&serde_json::json!({
                "user_id": user_id,
                "company_id": self.api_key.split(':').next().unwrap_or_default(),
            }))
            .send()
            .await?;

        if !response.status().is_success() {
            return Err(Error::Auth(format!(
                "Failed to refresh user token: {}",
                response.status()
            )));
        }

        let user_token: UserToken = response.json().await?;
        Ok(user_token)
    }

    pub async fn revoke_user_access(&self, user_id: &str) -> Result<()> {
        let response = self.client
            .post(format!("{}/auth/user/revoke", self.base_url))
            .header("X-API-Key", &self.api_key)
            .json(&serde_json::json!({
                "user_id": user_id,
                "company_id": self.api_key.split(':').next().unwrap_or_default(),
            }))
            .send()
            .await?;

        if !response.status().is_success() {
            return Err(Error::Auth(format!(
                "Failed to revoke user access: {}",
                response.status()
            )));
        }

        Ok(())
    }

    pub async fn get_init_token(&self) -> Result<String> {
        let response = self.client
            .post(format!("{}/auth/token", self.base_url))
            .header("X-API-Key", &self.api_key)
            .send()
            .await?;

        if !response.status().is_success() {
            return Err(Error::Auth(format!(
                "Failed to get initial token: {}",
                response.status()
            )));
        }

        let token_response: TokenResponse = response.json().await?;

        let token_data = TokenData {
            access_token: token_response.access_token,
            expires_at: Instant::now() + std::time::Duration::from_secs(token_response.expires_in as u64),
        };

        *self.token.write().await = Some(token_data.clone());
        Ok(token_data.access_token)
    }

    pub async fn get_valid_token(&self) -> Result<String> {
        if let Some(token_data) = self.token.read().await.as_ref() {
            if token_data.expires_at > Instant::now() {
                return Ok(token_data.access_token.clone());
            }
        }

        self.refresh_token().await
    }

    async fn refresh_token(&self) -> Result<String> {
        let response = self.client
            .post(&format!("{}/auth/token", self.base_url))
            .header("Authorization", format!("Bearer {}", self.api_key))
            .send()
            .await
            .map_err(|e| Error::Auth(format!("Failed to refresh token: {}", e)))?;

        if !response.status().is_success() {
            return Err(Error::Auth(format!(
                "Failed to refresh token: HTTP {}",
                response.status()
            )));
        }

        let token_response: TokenResponse = response
            .json()
            .await
            .map_err(|e| Error::Auth(format!("Failed to parse token response: {}", e)))?;

        let token_data = TokenData {
            access_token: token_response.access_token,
            expires_at: Instant::now() + std::time::Duration::from_secs(token_response.expires_in as u64),
        };

        *self.token.write().await = Some(token_data.clone());
        Ok(token_data.access_token)
    }

    pub async fn revoke_token(&self) -> Result<()> {
        let token = match self.token.read().await.as_ref() {
            Some(token_data) => token_data.access_token.clone(),
            None => return Err(Error::Auth("No token available for revocation".to_string())),
        };

        let response = self.client
            .post(&format!("{}/auth/revoke", self.base_url))
            .header("Authorization", format!("Bearer {}", token))
            .send()
            .await
            .map_err(|e| Error::Auth(format!("Failed to revoke token: {}", e)))?;

        if !response.status().is_success() {
            return Err(Error::Auth(format!(
                "Failed to revoke token: HTTP {}",
                response.status()
            )));
        }

        *self.token.write().await = None;
        Ok(())
    }
} 