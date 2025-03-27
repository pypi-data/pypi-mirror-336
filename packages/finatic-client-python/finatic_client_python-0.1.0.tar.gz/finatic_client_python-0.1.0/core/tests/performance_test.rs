use finatic_core::api::ApiClient;
use finatic_core::error::Error;
use std::time::Instant;

#[tokio::test]
async fn test_performance_concurrent_requests() {
    let client = ApiClient::new("test_key");
    let start = Instant::now();
    
    let mut handles = vec![];
    for _ in 0..100 {
        let client = client.clone();
        handles.push(tokio::spawn(async move {
            client.get_user_data().await
        }));
    }
    
    let results = futures::future::join_all(handles).await;
    let duration = start.elapsed();
    
    assert!(duration.as_millis() < 5000); // Should complete within 5 seconds
    assert!(results.iter().all(|r| r.is_ok()));
}

#[tokio::test]
async fn test_performance_large_response() {
    let client = ApiClient::new("test_key");
    let start = Instant::now();
    
    // Test with a large portfolio response
    let result = client.get_portfolio().await;
    let duration = start.elapsed();
    
    assert!(duration.as_millis() < 1000); // Should complete within 1 second
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_performance_memory_usage() {
    let client = ApiClient::new("test_key");
    let mut handles = vec![];
    
    // Create many concurrent requests to test memory usage
    for _ in 0..1000 {
        let client = client.clone();
        handles.push(tokio::spawn(async move {
            client.get_user_data().await
        }));
    }
    
    let results = futures::future::join_all(handles).await;
    assert!(results.iter().all(|r| r.is_ok()));
} 