# Monapi SDK for Python

This SDK allows providers to easily integrate with the Monapi Marketplace.

## Installation

```bash
pip install monapi-sdk
```

## Usage

```python
from fastapi import FastAPI, Request
from monapi import MarketplaceProvider
import os

app = FastAPI()

# Initialize the marketplace provider with your secret key
marketplace = MarketplaceProvider(
    provider_secret=os.getenv("MARKETPLACE_SECRET"),
)

# Add the marketplace middleware to validate incoming requests
@app.middleware("http")
async def marketplace_middleware(request: Request, call_next):
    return await marketplace.validate_request_middleware(request, call_next)

# Create your API endpoints
@app.post("/api/webhook")
async def handle_webhook(request: Request):
    # The request has already been validated by the middleware
    # You can now process the webhook
    data = await request.json()
    return {"status": "success", "data": data}
```

## Features

- Request validation using HMAC-SHA256 signatures
- FastAPI middleware for easy integration
- Automatic timestamp validation
- Detailed logging for debugging

## Requirements

- Python 3.7+
- FastAPI

## License

MIT 