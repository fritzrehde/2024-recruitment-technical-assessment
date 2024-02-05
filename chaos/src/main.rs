use axum::http::StatusCode;
use axum::{response::IntoResponse, routing::post, Json, Router};
use serde::{Deserialize, Serialize};

mod data;

#[tokio::main]
async fn main() {
    let app = Router::new().route("/process_data", post(data::process_data));

    axum::Server::bind(&"127.0.0.1:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}
