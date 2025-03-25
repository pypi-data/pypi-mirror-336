# liberal_alpha/client.py
#!/usr/bin/env python3
import grpc
import json
import time
import threading
import logging
import asyncio

from .exceptions import ConnectionError, RequestError
from .proto import service_pb2, service_pb2_grpc
from .subscriber import main_async
from .crypto import get_wallet_address

logger = logging.getLogger(__name__)

class LiberalAlphaClient:
    """
    Liberal Alpha SDK Client for sending data via gRPC and subscribing to WebSocket data.
    
    Parameters:
      - host (optional, default "127.0.0.1")
      - port (optional, default 8128)
      - rate_limit_enabled (optional, default True)
      - api_key (optional; required for subscribing to data)
      - private_key (optional; required for subscribing to data)
    
    The wallet address is automatically computed from the private key.
    The base URL is fixed to "http://34.143.214.250:8080" (will be updated later).
    """
    
    def __init__(self, host=None, port=None, rate_limit_enabled=None, api_key=None, private_key=None):
        self.host = host if host is not None else "127.0.0.1"
        self.port = port if port is not None else 8128
        self.rate_limit_enabled = rate_limit_enabled if rate_limit_enabled is not None else True
        self.api_key = api_key
        self.private_key = private_key
        # Wallet is computed automatically from private_key (if provided)
        self.wallet = get_wallet_address(private_key) if private_key else None
        # Base URL is fixed
        self.base_url = "http://34.143.214.250:8080"
        self._lock = threading.Lock()
        try:
            self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
            self.stub = service_pb2_grpc.JsonServiceStub(self.channel)
            grpc.channel_ready_future(self.channel).result(timeout=5)
        except grpc.RpcError as e:
            raise ConnectionError(details=str(e))
    
    def send_data(self, identifier: str, data: dict, record_id: str):
        """
        Send data via gRPC.
        This method does not require API key and private key checks.
        If the request fails, it is likely that no runner is running.
        """
        try:
            return self._send_request(identifier, data, "raw", record_id)
        except grpc.RpcError as e:
            raise RequestError(
                message="Failed to send gRPC request. No runner is running. Please start the runner.",
                code=e.code().value if e.code() else None,
                details=str(e.details())
            )
    
    def send_alpha(self, identifier: str, data: dict, record_id: str):
        """
        Send alpha signal via gRPC.
        This method does not require API key and private key checks.
        If the request fails, it is likely that no runner is running.
        """
        try:
            return self._send_request(identifier, data, "raw", record_id)
        except grpc.RpcError as e:
            raise RequestError(
                message="Failed to send gRPC request. No runner is running. Please start the runner.",
                code=e.code().value if e.code() else None,
                details=str(e.details())
            )
    
    def _send_request(self, identifier: str, data: dict, event_type: str, record_id: str):
        # Check if host and port are provided; if not, raise an error.
        if not self.host or not self.port:
            raise ValueError("Client is missing host and port parameters")
        
        with self._lock:
            current_time_ms = int(time.time() * 1000)
            metadata = {
                "source": "liberal_alpha_sdk",
                "entry_id": identifier,
                "record_id": record_id,
                "timestamp_ms": str(current_time_ms)
            }
            request = service_pb2.JsonRequest(
                json_data=json.dumps(data),
                event_type=event_type,
                timestamp=current_time_ms,
                metadata=metadata
            )
            response = self.stub.ProcessJson(request)
            logger.info(f"gRPC Response: {response}")
            return {
                "status": response.status,
                "message": response.message,
                "result": json.loads(response.result_json) if response.result_json else None,
                "error": response.error if response.error else None
            }
    
    def subscribe_data(self, record_id=None, max_reconnect=5, on_message: callable = None):
        """
        Subscribe to real-time data via WebSocket.
        This method requires that both API key and private key are provided.
        """
        if not self.api_key or not self.private_key:
            logger.error("API key and private key must be provided for subscribing to data.")
            return
        try:
            asyncio.run(
                main_async(api_key=self.api_key, base_url=self.base_url, wallet_address=self.wallet,
                           private_key=self.private_key, record_id=record_id,
                           max_reconnect=max_reconnect, on_message=on_message)
            )
        except KeyboardInterrupt:
            logger.info("Subscription interrupted by user")
        except Exception as e:
            logger.error(f"Error during subscription: {e}")

liberal = None

def initialize(host=None, port=None, rate_limit_enabled=None, api_key=None, private_key=None):
    global liberal
    liberal = LiberalAlphaClient(host, port, rate_limit_enabled, api_key, private_key)
    logger.info(f"SDK initialized: liberal={liberal}")
