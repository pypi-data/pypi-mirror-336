import os
import inspect
import time
import datetime
import platform
import uuid
import socket
from functools import wraps, lru_cache
import json
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar, cast
import logging
from concurrent.futures import ThreadPoolExecutor
import atexit

logger = logging.getLogger("janus")
F = TypeVar('F', bound=Callable[..., Any])

API_VERIFY_URL = "https://www.withjanus.com/api/verify"
API_TRACK_URL = "https://www.withjanus.com/api/track"

def _import_module(module_name: str) -> Any:
    import importlib
    return importlib.import_module(module_name)

class Janus:
    def __init__(
        self, 
        api_key: Optional[str] = None,
        timeout: int = 10,
        async_tracking: bool = True,
        max_workers: int = 2,
        debug: bool = False
    ):
        self.api_key = api_key
        self.timeout = timeout
        self.async_tracking = async_tracking
        self._system_info_cache = None
        self._metadata_cache = {}
        self._requests_session = None
        self.debug = debug
        
        if self.debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
            
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        logger.debug("Janus instance created with debug=%s", self.debug)
            
        if self.async_tracking:
            self._pool = ThreadPoolExecutor(max_workers=max_workers)
            atexit.register(self._cleanup)
        else:
            self._pool = None

    def _cleanup(self) -> None:
        logger.debug("Cleaning up resources.")
        if self._pool:
            self._pool.shutdown(wait=False)
        if self._requests_session:
            try:
                self._requests_session.close()
            except Exception as e:
                logger.debug("Error closing requests session: %s", e)

    @property
    def _session(self):
        if self._requests_session is None:
            requests = _import_module("requests")
            self._requests_session = requests.Session()
            if self.api_key:
                self._requests_session.headers.update({
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                })
            else:
                self._requests_session.headers.update({
                    "Content-Type": "application/json"
                })
            logger.debug("Requests session created with headers: %s", self._requests_session.headers)
        return self._requests_session

    @lru_cache(maxsize=128)
    def _get_function_metadata(self, function: Callable) -> Dict[str, Any]:
        try:
            source_code = inspect.getsource(function)
        except Exception:
            source_code = "Source not available"
        signature = inspect.signature(function)
        annotations = function.__annotations__
        sanitized_annotations = {k: str(v) for k, v in annotations.items()} if annotations else {}
        metadata = {
            "name": function.__name__,
            "module": function.__module__,
            "docstring": function.__doc__,
            "annotations": sanitized_annotations,
            "signature": str(signature),
            "source_code": source_code
        }
        logger.debug("Function metadata for '%s': %s", function.__name__, metadata)
        return metadata
    
    def _get_system_info(self) -> Dict[str, Any]:
        if self._system_info_cache is None:
            self._system_info_cache = {
                "os": platform.system(),
                "os_version": platform.version(),
                "machine": platform.machine(),
                "python_version": platform.python_version(),
                "python_implementation": platform.python_implementation(),
                "hostname": socket.gethostname()
            }
            logger.debug("Cached system info: %s", self._system_info_cache)
        psutil = _import_module("psutil")
        process = psutil.Process(os.getpid())
        dynamic_info = {
            "working_directory": os.getcwd(),
            "cpu_count": os.cpu_count(),
            "memory_usage_bytes": process.memory_info().rss
        }
        if hasattr(os, 'getloadavg'):
            dynamic_info["load_avg"] = os.getloadavg()
        system_info = {**self._system_info_cache, **dynamic_info}
        logger.debug("Dynamic system info: %s", dynamic_info)
        return system_info

    def _extract_data(self, function: Callable, args: Tuple, kwargs: Dict) -> Dict[str, Any]:
        record = {"call_id": str(uuid.uuid4())}
        record["function_info"] = self._get_function_metadata(function)
        signature = inspect.signature(function)
        try:
            bound_args = signature.bind(*args, **kwargs)
            bound_args.apply_defaults()
            sanitized_args = {}
            for key, value in bound_args.arguments.items():
                try:
                    json.dumps({key: value})
                    sanitized_args[key] = value
                except (TypeError, OverflowError):
                    sanitized_args[key] = str(value)
            record["function_info"]["bound_arguments"] = sanitized_args
            logger.debug("Bound arguments for '%s': %s", function.__name__, sanitized_args)
        except TypeError as e:
            record["function_info"]["bound_arguments"] = f"Error binding arguments: {e}"
            logger.debug("Error binding arguments for '%s': %s", function.__name__, e)
        frame = inspect.currentframe()
        try:
            caller_frame = frame.f_back.f_back
            record["function_info"]["caller_info"] = {
                "caller_function": caller_frame.f_code.co_name,
                "caller_module": caller_frame.f_globals.get("__name__", "unknown")
            }
        except (AttributeError, ValueError) as e:
            record["function_info"]["caller_info"] = {"caller_function": "unknown", "caller_module": "unknown"}
            logger.debug("Error retrieving caller info: %s", e)
        finally:
            del frame
        record["function_info"]["timestamp"] = datetime.datetime.now().isoformat()
        record["system_info"] = self._get_system_info()
        logger.debug("Extracted record: %s", record)
        return record
        
    def _api_request(
        self, 
        method: str, 
        url: str, 
        data: Optional[Dict] = None,
        retry_count: int = 2,
        backoff_factor: float = 0.5
    ) -> Optional[Any]:
        for attempt in range(retry_count + 1):
            try:
                logger.debug("API Request attempt %d: %s %s with data %s", attempt+1, method, url, data)
                if method.upper() == "GET":
                    response = self._session.get(url, timeout=self.timeout)
                elif method.upper() == "POST":
                    response = self._session.post(url, json=data, timeout=self.timeout)
                elif method.upper() == "PATCH":
                    response = self._session.patch(url, json=data, timeout=self.timeout)
                else:
                    logger.error("Unsupported HTTP method: %s", method)
                    return None
                logger.debug("Received response: %s for %s", response.status_code, url)
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', backoff_factor * (2 ** attempt)))
                    logger.debug("Rate limited. Retry after: %s seconds", retry_after)
                    if attempt < retry_count:
                        time.sleep(retry_after)
                        continue
                return response
            except Exception as e:
                logger.debug("API request error on attempt %d: %s", attempt+1, e)
                if attempt < retry_count:
                    time.sleep(backoff_factor * (2 ** attempt))
                else:
                    logger.warning("API request failed: %s", e)
                    return None
        return None

    def _get_decision(self, record: Dict[str, Any]) -> Tuple[str, str, Optional[str]]:
        if not API_VERIFY_URL:
            logger.debug("API_VERIFY_URL not configured.")
            return "rejected", "API URL not configured", None
        logger.debug("Starting decision process.")
        response = self._api_request("POST", API_VERIFY_URL, data=record)
        if not response or response.status_code != 200:
            status = response.status_code if response else 'connection error'
            logger.debug("API error during decision process: %s", status)
            return "rejected", f"API error: {status}", None
        try:
            data = response.json()
        except Exception as e:
            logger.debug("Error parsing JSON response: %s", e)
            return "rejected", "Invalid API response", None
        verification_id = data.get("verification_id")
        if not verification_id:
            logger.debug("No verification ID received in response.")
            return "rejected", "No verification ID received", None
        poll_url = f"{API_VERIFY_URL}/{verification_id}"
        deadline = time.perf_counter() + self.timeout
        wait_time = 0.1
        while time.perf_counter() < deadline:
            poll_response = self._api_request("GET", poll_url)
            if poll_response and poll_response.status_code == 200:
                try:
                    poll_data = poll_response.json()
                    decision = poll_data.get("decision")
                    logger.debug("Polling decision: decision=%s", decision)
                    if decision not in ("pending", None):
                        return decision, poll_data.get("comment", ""), verification_id
                except Exception as e:
                    logger.debug("Error polling decision: %s", e)
            time.sleep(min(wait_time, 1.0))
            wait_time *= 1.5
        logger.debug("Decision process timed out.")
        return "rejected", "Timeout waiting for decision", verification_id

    def track(self, function: F) -> F:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            call_id = str(uuid.uuid4())
            logger.debug("Tracking function '%s' with call_id: %s", function.__name__, call_id)
            record = self._extract_data(function, args, kwargs)
            record["status"] = "track"
            record["call_id"] = call_id
            time_start = time.perf_counter()
            try:
                result = function(*args, **kwargs)
                success = True
            except Exception as e:
                result = str(e)
                success = False
                logger.debug("Exception in function '%s': %s", function.__name__, e)
                raise
            finally:
                time_end = time.perf_counter()
                duration = round(time_end - time_start, 4)
                logger.debug("Function '%s' executed in %s seconds", function.__name__, duration)
                def record_execution():
                    record["execution"] = {
                        "timestamp": datetime.datetime.now().isoformat(),
                        "duration_sec": duration,
                        "success": success,
                        "output": str(result) if success else None
                    }
                    self._api_request("POST", API_TRACK_URL, data=record)
                    logger.debug("Execution record submitted for '%s'", function.__name__)
                if self.async_tracking and self._pool:
                    self._pool.submit(record_execution)
                else:
                    record_execution()
            return result
        return cast(F, wrapper)

    def verify(self, function: F) -> F:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            record = self._extract_data(function, args, kwargs)
            record["status"] = "verify"
            record["verification"] = {
                "request_time": datetime.datetime.now().isoformat()
            }
            logger.debug("Starting verification for function '%s'", function.__name__)
            decision_start = time.perf_counter()
            decision, comment, verification_id = self._get_decision(record)
            decision_end = time.perf_counter()
            record["verification"].update({
                "decision_time": datetime.datetime.now().isoformat(),
                "duration": round(decision_end - decision_start, 4),
                "decision": decision,
                "comment": comment
            })
            record["execution"] = {}
            if decision == "approved":
                time_start = time.perf_counter()
                try:
                    result = function(*args, **kwargs)
                    success = True
                except Exception as e:
                    result = str(e)
                    success = False
                    logger.debug("Exception during approved execution of '%s': %s", function.__name__, e)
                    raise
                finally:
                    time_end = time.perf_counter()
                    record["execution"].update({
                        "timestamp": datetime.datetime.now().isoformat(),
                        "duration_sec": round(time_end - time_start, 4),
                        "success": success,
                        "output": str(result) if success else None
                    })
                    def update_record():
                        if verification_id:
                            self._api_request("PATCH", f"{API_VERIFY_URL}/{verification_id}", data=record)
                            logger.debug("Updated verification record for '%s'", function.__name__)
                    if self.async_tracking and self._pool:
                        self._pool.submit(update_record)
                    else:
                        update_record()
            else:
                record["execution"]["output"] = "rejected"
                result = None
                logger.debug("Function '%s' verification rejected.", function.__name__)
                if verification_id:
                    self._api_request("PATCH", f"{API_VERIFY_URL}/{verification_id}", data=record)
            return result
        return cast(F, wrapper)