from azure.core.credentials import TokenCredential
import redis
import asyncio
# from ...base_connector import BaseConnector

class AzureRedisClientError(Exception):
    """Base exception for BingGroundingClient errors."""
    pass

class AzureRedisClient():
    def __init__(
        self,
        *,
        token_credential: TokenCredential,
        scope: str = None,
        host: str,
        port: int,
        username: str,
        **kwargs
    ) -> None:
        if token_credential is None:
            raise AzureRedisClientError(
                "Missing token_credential. Please pass a valid TokenCredential instance."
            )
        # set up logger, tracer, metric_counter
        # super().__init__(
        #     token_credential=token_credential,
        #     logger=kwargs.get("logger"),
        #     tracer=kwargs.get("tracer"),
        #     metric_counter=kwargs.get("metric_counter")
        # )
        self._scope = scope
        self._host = host
        self._port = port
        self._username = username
        self._token_credential = token_credential
        self._client_sync = redis.Redis(
            host=self._host,
            port=self._port,
            ssl=True,
            username=self._username,
            password=self._token_credential.get_token(self._scope).token,
            decode_responses=True
        )
        self._client_async = redis.asyncio.Redis(
            host=self._host,
            port=self._port,
            ssl=True,
            username=self._username,
            password=self._token_credential.get_token(self._scope).token,
            decode_responses=True
        )
    
    def close(self):
        super().close()
        self._client_sync.close()
        self._client_async.close()
    
    def __enter__(self):
        return self._client_sync
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._client_sync.close()
    
    async def __aenter__(self):
        return self._client_async
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._client_async.close()
    