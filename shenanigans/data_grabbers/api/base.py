from loguru import logger
from typing import Optional, Tuple
from request_models.coingecko import Errors
import pydantic
import aiohttp
import asyncio
from time import time

class LeakyBucket:
    def __init__(self, capacity: int, fill_rate: float):
        """Initialize the leaky bucket rate limiter.

        Args:
            capacity (int): The maximum number of tokens in the bucket (i.e., requests allowed in a burst).
            fill_rate (float): The rate at which tokens are added to the bucket, in tokens per second.
        """
        self.capacity = capacity
        self._tokens = capacity
        self.fill_rate = fill_rate
        self.timestamp = time()

    def consume(self, tokens: int = 1) -> bool:
        """Consume tokens from the bucket. Returns True if the tokens were consumed, False otherwise.

        Args:
            tokens (int): The number of tokens to consume.

        Returns:
            bool: True if the tokens were successfully consumed, False otherwise.
        """
        if tokens <= self.get_tokens():
            self._tokens -= tokens
            return True
        return False

    def get_tokens(self) -> float:
        """Get the current number of tokens in the bucket, refilling it according to the elapsed time and fill rate."""
        now = time()
        if self._tokens < self.capacity:
            delta = self.fill_rate * (now - self.timestamp)
            self._tokens = min(self.capacity, self._tokens + delta)
        self.timestamp = now
        return self._tokens

class Interface:
    """A long-lived interface for making API requests with rate limiting and session management."""

    def __init__(self, base_url: str, global_rate_limit: Tuple[int, float]):
        # global_rate_limit = (100, 1/60)  - 100 requests per minute, refills at 1 request per second
        self.base_url: str = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.session_last_refresh: float = time()
        self.leaky_bucket: LeakyBucket = LeakyBucket(*global_rate_limit)
        self.headers = {}

    async def refresh_session(self) -> None:
        """Refreshes the client session if it's closed, None, or older than 10 minutes."""
        if self.session is None or self.session.closed or (time() - self.session_last_refresh) > 600:
            if self.session:
                await self.session.close()
            self.session = aiohttp.ClientSession()
            self.session_last_refresh = time()

    async def _rate_limit(self) -> None:
        """Waits until the rate limiter allows for another request to be made."""
        while not self.leaky_bucket.consume():
            logger.debug(f"...seems we are hitting the rate limit wall, waiting 1s")
            await asyncio.sleep(1)

    async def request(self, endpoint: str, method: str, **kwargs) -> dict:
        """A helper method to make HTTP requests."""
        await self._rate_limit()
        await self.refresh_session()
        url = f"{self.base_url}/{endpoint}"
        async with self.session.request(method, url, **kwargs) as response:
            result = await response.json()
            return result

    def validate_response(self, result, schemaObject):
        """Validate the response and log any issues."""
        try:
            Errors.Validator(**result)
        except pydantic.ValidationError:
            pass
        else:
            return False

        try:
            validated_result = schemaObject(**result)
        except pydantic.ValidationError:
            logger.warning("Result didn't match the expected shape of this request... check debug for the full schema of the return...")
            logger.debug(result)
            return False
        else:
            return validated_result

    async def close(self) -> None:
        """Closes the client session and waits for the queue to be processed."""
        if self.session:
            await self.session.close()
