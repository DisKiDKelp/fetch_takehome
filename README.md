# Fetch Takehome, Receipt Processor API

## Overview
Take home exercise for Fetch; The Receipt Processor API allows users to submit receipts for processing and retrieve the points awarded for a given receipt. The API is designed to handle structured receipt data and return a unique receipt ID upon successful processing. Users can then query the receipt by its ID to get the associated points.

## API Endpoints

### 1. Submit a Receipt for Processing
**Endpoint:** `POST /receipts/process`

**Description:**
Submits a receipt for processing and returns a unique receipt ID.

**Request Body:** (JSON)
```json
{
    "retailer": "M&M Corner Market",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
        }
    ],
    "total": "6.49"
}
```

**Response:** (Success - 200 OK)
```json
{
    "id": "adb6b560-0eef-42bc-9d16-df48f30e89b2"
}
```

**Error Responses:**
- `400 Bad Request`: The request is invalid.

---

### 2. Get Points for a Receipt
**Endpoint:** `GET /receipts/{id}/points`

**Description:**
Retrieves the number of points awarded for a given receipt by its unique ID.

**Path Parameter:**
- `id` (string, required) - The unique identifier for the receipt.

**Response:** (Success - 200 OK)
```json
{
    "points": 20
}
```

**Error Responses:**
- `404 Not Found`: No receipt found for the given ID.

## Data Models

### Receipt Object
| Property        | Type   | Description |
|----------------|--------|-------------|
| retailer       | string | The name of the retailer. |
| purchaseDate   | string (date) | The date of purchase in `YYYY-MM-DD` format. |
| purchaseTime   | string (time) | The time of purchase in `HH:MM` 24-hour format. |
| items         | array  | A list of purchased items. |
| total         | string | The total amount paid, formatted as a decimal string (e.g., "6.49"). |

### Item Object
| Property          | Type   | Description |
|------------------|--------|-------------|
| shortDescription | string | A brief description of the item. |
| price           | string | The total price of the item, formatted as a decimal string. |

## Error Handling
- `400 Bad Request`: Returned when the request body is invalid or missing required fields.
- `404 Not Found`: Returned when the requested receipt ID does not exist.

## Example Usage

Must first build the container via docker and run it with the command:
```
docker build . --no-cache -t receipt_processor && docker run -p 8080:8080 receipt_processor
```


### Submitting a Receipt
```bash
curl -X POST "http://0.0.0.0:8080/receipts/process" \
     -H "Content-Type: application/json" \
     -d '{
         "retailer": "M&M Corner Market",
         "purchaseDate": "2022-01-01",
         "purchaseTime": "13:01",
         "items": [{
             "shortDescription": "Mountain Dew 12PK",
             "price": "6.49"
         }],
         "total": "6.49"
     }'
```

### Retrieving Points for a Receipt

Grab the ID from the previous response and put it in a following GET curl, i.e.

```bash
curl -X GET "http://0.0.0.0:8080/receipts/61727a71-a247-40cd-b843-2d96b1c4e6b7/points"
```


