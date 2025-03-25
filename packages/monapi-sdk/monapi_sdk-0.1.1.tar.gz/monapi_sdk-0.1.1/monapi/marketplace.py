import hashlib
import hmac
import json
import logging
import time
from typing import Any, Dict, Optional

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

# Set up logging
logger = logging.getLogger(__name__)


class MarketplaceProvider:
    def __init__(
        self,
        provider_secret: str,
        base_url: str = "https://monapi-router.onrender.com",
        timeout: float = 30.0,
    ):
        self.provider_secret = provider_secret
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        logger.info(f"MarketplaceProvider initialized with base_url: {self.base_url}")

    async def validate_request(self, request: Request) -> bool:
        """
        Validate that a request came from the marketplace

        Args:
            request: FastAPI Request object

        Returns:
            bool: True if request is valid, False otherwise
        """
        # Log detailed request information for testing
        logger.info("=" * 50)
        logger.info(f"INCOMING REQUEST: {request.method} {request.url.path}")
        logger.info(f"Client: {request.client.host if request.client else 'Unknown'}")
        logger.info("Headers:")
        for header_name, header_value in request.headers.items():
            logger.info(f"  {header_name}: {header_value}")
        
        # Extract and log query parameters
        query_params = dict(request.query_params)
        if query_params:
            logger.info("Query Parameters:")
            for param, value in query_params.items():
                logger.info(f"  {param}: {value}")
        
        signature = request.headers.get("X-Marketplace-Signature")
        timestamp = request.headers.get("X-Marketplace-Timestamp")

        logger.info(
            f"Validating request with signature: {signature}, timestamp: {timestamp}"
        )

        if not all([signature, timestamp]):
            logger.error("Missing signature or timestamp")
            return False

        # Check timestamp freshness (5 minute window)
        try:
            ts = int(timestamp)
            current_time = int(time.time())
            time_diff = abs(current_time - ts)
            logger.info(f"Current time: {current_time}, Request time: {ts}, Difference: {time_diff} seconds")
            
            if time_diff > 300:
                logger.error(f"Timestamp too old: {time_diff} seconds difference exceeds 300 second window")
                return False
        except ValueError:
            logger.error("Invalid timestamp format")
            return False

        # Calculate expected signature
        try:
            # Read the request body and store it
            body = await request.body()
            
            # Store the body in request.state instead of modifying _receive
            request.state.raw_body = body
            
            logger.info(f"Request body: {body.decode() if body else 'empty'}")

            if body:
                try:
                    # Parse the body as JSON to match router's json.dumps()
                    body_json = json.loads(body)
                    body_str = json.dumps(body_json)
                    logger.info(f"Parsed body JSON: {body_str}")
                    
                    # Store parsed body in state for reuse
                    request.state.parsed_body = body_json
                    
                    # Log specific fields of interest if they exist
                    if isinstance(body_json, dict):
                        logger.info("Key fields in request body:")
                        for key in ["action", "type", "id", "status", "event"]:
                            if key in body_json:
                                logger.info(f"  {key}: {body_json[key]}")
                except json.JSONDecodeError:
                    logger.error("Failed to parse body as JSON")
                    body_str = ""
            else:
                body_str = ""

            signature_input = f"{timestamp}{body_str}"
            logger.info(f"Signature input: {signature_input}")
            
            expected_signature = hmac.new(
                self.provider_secret.encode(),
                signature_input.encode(),
                hashlib.sha256,
            ).hexdigest()

            logger.info(f"Expected signature: {expected_signature}")
            logger.info(f"Received signature: {signature}")

            is_valid = hmac.compare_digest(signature, expected_signature)
            logger.info(
                f"Signature validation result: {'valid' if is_valid else 'invalid'}"
            )
            logger.info("=" * 50)

            return is_valid
        except Exception as e:
            logger.error(f"Error validating signature: {str(e)}")
            logger.exception("Full exception details:")
            return False

    async def validate_request_middleware(self, request: Request, call_next):
        """
        FastAPI middleware for validating marketplace requests

        Usage:
            app = FastAPI()
            marketplace = MarketplaceProvider(provider_secret="your_secret")
            app.middleware("http")(marketplace.validate_request_middleware)
        """
        # Log middleware execution
        logger.info(f"Middleware started for: {request.method} {request.url.path}")
        
        # Validate all requests
        validation_result = await self.validate_request(request)
        if not validation_result:
            logger.warning(f"Request validation failed for: {request.method} {request.url.path}")
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid credentials"}
            )

        logger.info(f"Request validation successful, proceeding with: {request.method} {request.url.path}")
        try:
            # Create a custom RequestScope that includes our stored body
            # This ensures FastAPI can read the body again
            logger.info(f"About to call endpoint handler for: {request.method} {request.url.path}")
            response = await call_next(request)
            logger.info(f"Endpoint handler completed for: {request.method} {request.url.path}")
            logger.info(f"Middleware completed for: {request.method} {request.url.path} with status: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"Error in middleware call_next: {str(e)}", exc_info=True)
            return JSONResponse(
                status_code=500,
                content={"error": f"Internal server error: {str(e)}"}
            ) 