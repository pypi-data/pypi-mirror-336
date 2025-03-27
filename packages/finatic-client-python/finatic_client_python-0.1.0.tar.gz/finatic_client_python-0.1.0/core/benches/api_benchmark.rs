use criterion::{black_box, criterion_group, criterion_main, Criterion};
use finatic_core::api::ApiClient;
use finatic_core::models::*;

fn bench_user_data(c: &mut Criterion) {
    let client = ApiClient::new("test_key");
    
    c.bench_function("get_user_data", |b| {
        b.to_async(tokio::runtime::Runtime::new().unwrap())
            .iter(|| black_box(client.get_user_data()));
    });
}

fn bench_portfolio(c: &mut Criterion) {
    let client = ApiClient::new("test_key");
    
    c.bench_function("get_portfolio", |b| {
        b.to_async(tokio::runtime::Runtime::new().unwrap())
            .iter(|| black_box(client.get_portfolio()));
    });
}

fn bench_order_placement(c: &mut Criterion) {
    let client = ApiClient::new("test_key");
    let order = OrderRequest {
        symbol: "AAPL".to_string(),
        side: OrderSide::Buy,
        quantity: 1,
        order_type: OrderType::Market,
        price: None,
        time_in_force: None,
    };
    
    c.bench_function("place_order", |b| {
        b.to_async(tokio::runtime::Runtime::new().unwrap())
            .iter(|| black_box(client.place_order(order.clone())));
    });
}

criterion_group!(
    benches,
    bench_user_data,
    bench_portfolio,
    bench_order_placement
);
criterion_main!(benches); 