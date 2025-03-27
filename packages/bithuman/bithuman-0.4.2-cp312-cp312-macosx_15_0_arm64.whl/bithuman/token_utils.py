"""Token utilities for BithumanRuntime."""
import asyncio
import datetime
from typing import Optional, Any, Dict, Union, Callable
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from loguru import logger
from dataclasses import dataclass
import aiohttp
import time

from bithuman.runtime import Bithuman
from bithuman.runtime_async import AsyncBithuman


class TokenRequestError(Exception):
    """Custom exception for token request errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response_text: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(self.message)

@dataclass
class TokenRequestConfig:
    """Configuration for token requests."""
    api_url: str
    api_secret: str
    client_id: Optional[str] = None
    figure_id: Optional[str] = None
    runtime_model_hash: Optional[str] = None
    tags: Optional[str] = None
    insecure: bool = False
    timeout: float = 30.0

    @classmethod
    def from_namespace(cls, namespace) -> 'TokenRequestConfig':
        """Create a TokenRequestConfig from an argparse.Namespace object.
        
        Args:
            namespace: An argparse.Namespace object containing the configuration
            
        Returns:
            TokenRequestConfig: A new TokenRequestConfig instance
        """
        # Get required parameters
        api_url = getattr(namespace, 'api_url', None)
        api_secret = getattr(namespace, 'api_secret', None)
        
        if not api_url or not api_secret:
            raise ValueError("api_url and api_secret are required parameters")
        
        # Get optional parameters with defaults
        return cls(
            api_url=api_url,
            api_secret=api_secret,
            client_id=getattr(namespace, 'client_id', None),
            figure_id=getattr(namespace, 'figure_id', None),
            runtime_model_hash=getattr(namespace, 'runtime_model_hash', None),
            tags=getattr(namespace, 'tags', None),
            insecure=getattr(namespace, 'insecure', False),
            timeout=getattr(namespace, 'timeout', 30.0)
        )


def _prepare_request_data(fingerprint: str, config: TokenRequestConfig) -> Dict[str, Any]:
    """Prepare request data for token request."""
    data = {"fingerprint": fingerprint}
    
    if hasattr(config, 'client_id') and config.client_id:
        data["client_id"] = config.client_id

    if hasattr(config, 'figure_id') and config.figure_id:
        data["figure_id"] = config.figure_id

    if hasattr(config, 'runtime_model_hash') and config.runtime_model_hash:
        data["runtime_model_hash"] = config.runtime_model_hash

    if hasattr(config, 'tags') and config.tags:
        data["tags"] = config.tags
    
    return data


def _prepare_headers(config: TokenRequestConfig) -> Dict[str, str]:
    """Prepare headers for token request."""
    headers = {"Content-Type": "application/json"}
    
    if config.api_secret:
        headers["api-secret"] = config.api_secret
        logger.debug("API secret provided")
    else:
        logger.warning("No api-secret provided, authentication may fail")
    
    return headers


def _prepare_session() -> requests.Session:
    """Prepare requests session with retry capability."""
    session = requests.Session()
    
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session


def _log_request_debug(headers: Dict[str, str], data: Dict[str, Any], api_url: str):
    """Log request debug information."""
    debug_headers = headers.copy()
    if "api-secret" in debug_headers:
        secret_val = debug_headers["api-secret"]
        debug_headers["api-secret"] = secret_val[:4] + "..." + secret_val[-4:] if len(secret_val) > 8 else "***"
    
    logger.debug(f"Request headers: {debug_headers}")
    logger.debug(f"Request data: {data}")
    logger.debug(f"Using API URL: {api_url}")


def _parse_response(response_data: Dict[str, Any], status_code: int, response_text: str) -> str:
    """Parse the response data and extract the token.
    
    Args:
        response_data: The parsed JSON response data
        status_code: The HTTP status code
        response_text: The raw response text
        
    Returns:
        str: The extracted token
        
    Raises:
        TokenRequestError: If the response is invalid or contains an error
    """
    if status_code == 200:
        if response_data.get("status") == "success" and "data" in response_data:
            token = response_data["data"]["token"]
            logger.debug("Successfully obtained token from API")
            return token
        else:
            error_msg = f"API returned error: {response_data}"
            logger.error(error_msg)
            raise TokenRequestError(error_msg, status_code, response_text)
    else:
        error_msg = f"Failed to get token. Status code: {status_code}, Response: {response_text}"
        logger.error(error_msg)
        raise TokenRequestError(error_msg, status_code, response_text)


def _handle_request_error(e: Exception) -> None:
    """Handle different types of request errors.
    
    Args:
        e: The exception that occurred
        
    Raises:
        TokenRequestError: With appropriate error message
    """
    if isinstance(e, requests.exceptions.SSLError):
        error_msg = f"SSL Error requesting token: {e}"
        logger.error(error_msg)
        logger.error("This might be fixed by using the --insecure flag if your environment has SSL issues.")
    elif isinstance(e, requests.exceptions.ConnectionError):
        error_msg = f"Connection Error requesting token: {e}"
        logger.error(error_msg)
        logger.error("Please check your network connection and the API URL.")
    elif isinstance(e, requests.exceptions.Timeout):
        error_msg = f"Timeout Error requesting token: {e}"
        logger.error(error_msg)
        logger.error("The API server took too long to respond.")
    else:
        error_msg = f"Error requesting token: {e}"
        logger.error(error_msg)
        logger.error(f"Exception type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
    
    raise TokenRequestError(error_msg)


def _prepare_request(runtime: Union[Bithuman, AsyncBithuman], config: Union[TokenRequestConfig, Any]) -> tuple[Dict[str, Any], Dict[str, str]]:
    """Prepare request data and headers for token request.
    
    Args:
        runtime: The BithumanRuntime instance (sync or async)
        config: The TokenRequestConfig for token requests or argparse.Namespace object
        
    Returns:
        tuple[Dict[str, Any], Dict[str, str]]: A tuple containing (request_data, headers)
    """
    # Convert namespace to TokenRequestConfig if needed
    if not isinstance(config, TokenRequestConfig):
        config = TokenRequestConfig.from_namespace(config)
    
    # Set runtime model hash if available
    if hasattr(runtime, 'model_hash'):
        config.runtime_model_hash = runtime.model_hash
    
    # Prepare request data
    data = _prepare_request_data(runtime.fingerprint, config)
    
    # Prepare headers
    headers = _prepare_headers(config)
    
    return data, headers


def request_token_sync(runtime: Bithuman, config: TokenRequestConfig) -> str:
    """Synchronous version of token request."""
    try:
        # Prepare request data and headers
        data, headers = _prepare_request(runtime, config)
        
        # Create session with retry capability
        session = _prepare_session()
        
        # Make request
        response = session.post(
            config.api_url,
            json=data,
            headers=headers,
            timeout=config.timeout
        )
        
        # Log response details
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {dict(response.headers)}")
        logger.debug(f"Response body: {response.text}")
        
        # Parse response
        return _parse_response(response.json(), response.status_code, response.text)
            
    except Exception as e:
        _handle_request_error(e)


async def request_token_async(runtime: AsyncBithuman, config: TokenRequestConfig) -> str:
    """Asynchronous version of token request."""
    try:
        # Prepare request data and headers
        data, headers = _prepare_request(runtime, config)
        
        # Configure SSL context if needed
        ssl_context = None if not config.insecure else False
        
        # Make request with retry logic
        for attempt in range(3):  # Try up to 3 times
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        config.api_url,
                        json=data,
                        headers=headers,
                        ssl=ssl_context,
                        timeout=config.timeout
                    ) as response:
                        # Log response details
                        logger.debug(f"Response status: {response.status}")
                        logger.debug(f"Response headers: {dict(response.headers)}")
                        response_text = await response.text()
                        logger.debug(f"Response body: {response_text}")
                        
                        # Parse response
                        return _parse_response(
                            await response.json(),
                            response.status,
                            response_text
                        )
                            
            except aiohttp.ClientError as e:
                if attempt == 2:  # Last attempt
                    error_msg = f"Failed after 3 attempts: {e}"
                    logger.error(error_msg)
                    raise TokenRequestError(error_msg)
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                await asyncio.sleep(1)  # Wait before retrying
                
    except Exception as e:
        _handle_request_error(e)


async def _handle_token_refresh(
    runtime: Union[Bithuman, AsyncBithuman],
    token: str,
    on_token_refresh: Optional[Callable[[str], None]] = None
) -> bool:
    """Handle token refresh validation and setting.

    Args:
        runtime: The BithumanRuntime instance.
        token: The token to validate and set.
        on_token_refresh: Optional callback function to be called after successful token refresh.

    Returns:
        bool: True if token refresh was successful, False otherwise.
    """
    try:
        logger.debug("Validating and setting refreshed token")
        if isinstance(runtime, AsyncBithuman):
            await runtime.set_token(token)
        else:
            runtime.set_token(token)
        logger.debug(f"Token refreshed successfully at {datetime.datetime.now()}")
        if on_token_refresh:
            on_token_refresh(token)
        return True
    except Exception as e:
        logger.error(f"Error during token refresh: {e}")
        return False


async def token_refresh_worker_async(
    runtime: AsyncBithuman,
    config: TokenRequestConfig,
    stop_event: asyncio.Event,
    refresh_interval: int = 60,
    error_retry_interval: int = 5,
    on_token_refresh: Optional[Callable[[str], None]] = None
) -> None:
    """Asynchronous version of token refresh worker.

    Args:
        runtime: The AsyncBithuman instance.
        config: The TokenRequestConfig for token requests.
        stop_event: An asyncio.Event to control the worker loop.
        refresh_interval: Time in seconds between token refreshes (default: 60).
        error_retry_interval: Time in seconds to wait after an error before retrying (default: 5).
        on_token_refresh: Optional callback function to be called after successful token refresh.
    """
    while not stop_event.is_set():
        try:
            # Request a new token
            token = await request_token_async(runtime, config)
            if token:
                await _handle_token_refresh(runtime, token, on_token_refresh)
            else:
                logger.error("Failed to refresh token")

            # Wait for refresh_interval seconds before the next refresh,
            # checking for stop event every second
            for _ in range(refresh_interval):
                if stop_event.is_set():
                    break
                await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"Error in token refresh thread: {e}")
            # Wait error_retry_interval seconds before retrying after an error
            await asyncio.sleep(error_retry_interval)


def token_refresh_worker_sync(
    runtime: Bithuman,
    config: TokenRequestConfig,
    stop_event: asyncio.Event,
    refresh_interval: int = 60,
    error_retry_interval: int = 5,
    on_token_refresh: Optional[Callable[[str], None]] = None
) -> None:
    """Synchronous version of token refresh worker.

    Args:
        runtime: The BithumanRuntime instance.
        config: The TokenRequestConfig for token requests.
        stop_event: An asyncio.Event to control the worker loop.
        refresh_interval: Time in seconds between token refreshes (default: 60).
        error_retry_interval: Time in seconds to wait after an error before retrying (default: 5).
        on_token_refresh: Optional callback function to be called after successful token refresh.
    """
    while not stop_event.is_set():
        try:
            # Request a new token
            token = request_token_sync(runtime, config)
            if token:
                asyncio.run(_handle_token_refresh(runtime, token, on_token_refresh))
            else:
                logger.error("Failed to refresh token")

            # Wait for refresh_interval seconds before the next refresh,
            # checking for stop event every second
            for _ in range(refresh_interval):
                if stop_event.is_set():
                    break
                time.sleep(1)

        except Exception as e:
            logger.error(f"Error in token refresh thread: {e}")
            # Wait error_retry_interval seconds before retrying after an error
            time.sleep(error_retry_interval)
