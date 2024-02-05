use axum::response::IntoResponse;
use axum::Json;
use serde::{Deserialize, Serialize};

pub async fn process_data(Json(request): Json<DataRequest>) -> impl IntoResponse {
    // TODO: Calculate sums and return response

    let (string_len, int_sum) =
        request
            .data
            .iter()
            .fold((0, 0), |(string_len_acc, int_sum_acc), data| match data {
                Data::String(s) => (string_len_acc + s.len(), int_sum_acc),
                Data::Int(i) => (string_len_acc, int_sum_acc + i),
            });

    let response = DataResponse {
        string_len,
        int_sum,
    };

    (axum::http::StatusCode::OK, Json(response))
}

#[derive(Deserialize)]
pub struct DataRequest {
    // TODO: Add any fields here
    data: Vec<Data>,
}

#[derive(Deserialize)]
#[serde(untagged)]
enum Data {
    String(String),
    Int(usize),
}

#[derive(Serialize)]
struct DataResponse {
    // TODO: Add any fields here
    string_len: usize,
    int_sum: usize,
}
