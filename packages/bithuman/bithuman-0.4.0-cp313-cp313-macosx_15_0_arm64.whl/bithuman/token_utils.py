"""Token utilities for BithumanRuntime."""
import asyncio
import datetime
from typing import Optional, Any, Dict, Union
import urllib3
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from loguru import logger


class TokenRequestConfig:
    """Configuration for token requests."""
    def __init__(
        self,
        api_url: str = "https://api.one.bithuman.io/v1/runtime-tokens/request",
        client_id: Optional[str] = None,
        api_secret: Optional[str] = None,
        figure_id: Optional[str] = None,
        tags: Optional[str] = None,
        insecure: bool = False,
        timeout: int = 15,
    ):
        self.api_url = api_url
        self.client_id = client_id
        self.api_secret = api_secret
        self.figure_id = figure_id
        self.tags = tags
        self.insecure = insecure
        self.timeout = timeout


def _prepare_request_data(fingerprint: str, config: TokenRequestConfig) -> Dict[str, Any]:
    """Prepare request data for token request."""
    data = {"fingerprint": fingerprint}
    
    if config.figure_id:
        data["figure_id"] = config.figure_id
    
    if config.tags:
        data["tags"] = config.tags
    
    return data


def _prepare_headers(config: TokenRequestConfig) -> Dict[str, str]:
    """Prepare headers for token request."""
    headers = {"Content-Type": "application/json"}
    
    if config.client_id:
        headers["client-id"] = config.client_id
        logger.debug(f"Using client-id: {config.client_id}")
    else:
        logger.warning("No client-id provided, authentication may fail")
    
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


async def request_token_async(runtime: Any, config: TokenRequestConfig) -> Optional[str]:
    """Request a token from the API asynchronously."""
    try:
        data = _prepare_request_data(runtime.print_fingerprint, config)
        headers = _prepare_headers(config)
        _log_request_debug(headers, data, config.api_url)
        
        verify_ssl = not config.insecure
        if not verify_ssl:
            logger.warning("SSL verification is disabled. This is not recommended for production use.")
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        session = _prepare_session()
        
        logger.info(f"Requesting token from API at {datetime.datetime.now()}...")
        
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: session.post(
                config.api_url,
                headers=headers,
                json=data,
                timeout=config.timeout,
                verify=verify_ssl
            )
        )
        
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {dict(response.headers)}")
        logger.debug(f"Response body: {response.text}")
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("status") == "success" and "data" in response_data:
                token = response_data["data"]["token"]
                logger.info("Successfully obtained token from API")
                return token
            else:
                logger.error(f"API returned error: {response_data}")
                return None
        else:
            logger.error(f"Failed to get token. Status code: {response.status_code}, Response: {response.text}")
            return None
            
    except requests.exceptions.SSLError as e:
        logger.error(f"SSL Error requesting token: {e}")
        logger.error("This might be fixed by using the --insecure flag if your environment has SSL issues.")
        return None
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection Error requesting token: {e}")
        logger.error("Please check your network connection and the API URL.")
        return None
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout Error requesting token: {e}")
        logger.error("The API server took too long to respond.")
        return None
    except Exception as e:
        logger.error(f"Error requesting token: {e}")
        logger.error(f"Exception type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return None


def request_token_sync(runtime: Any, config: TokenRequestConfig) -> Optional[str]:
    """Request a token from the API synchronously."""
    try:
        data = _prepare_request_data(runtime.print_fingerprint, config)
        headers = _prepare_headers(config)
        _log_request_debug(headers, data, config.api_url)
        
        session = _prepare_session()
        
        logger.info(f"Requesting token from API at {datetime.datetime.now()}...")
        response = session.post(
            config.api_url,
            headers=headers,
            json=data,
            timeout=config.timeout
        )
        
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {dict(response.headers)}")
        logger.debug(f"Response body: {response.text}")
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("status") == "success" and "data" in response_data:
                token = response_data["data"]["token"]
                logger.info("Successfully obtained token from API")
                return token
            else:
                logger.error(f"API returned error: {response_data}")
                return None
        else:
            logger.error(f"Failed to get token. Status code: {response.status_code}, Response: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Error requesting token: {e}")
        logger.error(f"Exception type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return None 