#!/usr/bin/env python3
import grpc
import json
import time
import threading
import logging
import asyncio

from .config import SDKConfig
from .exceptions import ConnectionError, RequestError
from .proto import service_pb2, service_pb2_grpc
from .subscriber import main_async  # 从 subscriber 模块引入
from .crypto import get_public_key_from_private

logger = logging.getLogger(__name__)

class LiberalAlphaClient:
    """Liberal Alpha SDK Client for sending data via gRPC and subscribing to WebSocket data."""
    
    def __init__(self, host=None, port=None, rate_limit_enabled=None, api_key=None, private_key=None, wallet=None, base_url=None):
        self.host = host if host is not None else "127.0.0.1"
        self.port = port if port is not None else 8128
        self.rate_limit_enabled = rate_limit_enabled if rate_limit_enabled is not None else True
        self.api_key = api_key
        self.private_key = private_key
        self.wallet = wallet
        self.base_url = base_url
        self._lock = threading.Lock()
        try:
            self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
            self.stub = service_pb2_grpc.JsonServiceStub(self.channel)
            grpc.channel_ready_future(self.channel).result(timeout=5)
        except grpc.RpcError as e:
            raise ConnectionError(details=str(e))
    
    def send_data(self, identifier: str, data: dict, record_id: str):
        return self._send_request(identifier, data, "raw", record_id)
    
    def send_alpha(self, identifier: str, data: dict, record_id: str):
        return self._send_request(identifier, data, "raw", record_id)
    
    def _send_request(self, identifier: str, data: dict, event_type: str, record_id: str):
        with self._lock:
            try:
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
            except grpc.RpcError as e:
                raise RequestError(
                    message="Failed to send gRPC request",
                    code=e.code().value if e.code() else None,
                    details=str(e.details())
                )
    
    def subscribe_data(self, record_id=None, max_reconnect=5, on_message: callable = None):
        if not self.api_key:
            logger.error("api_key is not provided during initialization.")
            return
        if not self.private_key:
            logger.error("private_key is not provided during initialization.")
            return
        if not self.wallet:
            logger.error("wallet is not provided during initialization.")
            return
        if not self.base_url:
            logger.error("base_url is not provided during initialization.")
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

def initialize(host=None, port=None, rate_limit_enabled=None, api_key=None, private_key=None, wallet=None, base_url=None):
    global liberal
    liberal = LiberalAlphaClient(host, port, rate_limit_enabled, api_key, private_key, wallet, base_url)
    logger.info(f"SDK initialized: liberal={liberal}")
