import os
from typing import Optional
from dotenv import load_dotenv
from parallel import Parallel


class ParallelClient:
    """Wrapper class for the Parallel API client."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Parallel client.
        
        Args:
            api_key: Optional API key. If not provided, will look for
                     PARALLEL_API_KEY environment variable.
        """
        load_dotenv()
        
        self.api_key = api_key or os.getenv("PARALLEL_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Provide via argument or PARALLEL_API_KEY env var."
            )
        
        self._client = Parallel(api_key=self.api_key)
    
    @property
    def client(self) -> Parallel:
        """Return the underlying Parallel client."""
        return self._client
    
    def is_connected(self) -> bool:
        """Check if the client is properly configured."""
        return self._client is not None and self.api_key is not None


if __name__ == "__main__":
    client = ParallelClient(api_key="Bh5qbK7OhHVAl1NgDfyoT2oHjcA9DvHfyXQL8gp9")
    print(f"Client connected: {client.is_connected()}")
    print(f"API key configured: {'*' * 8}{client.api_key[-4:]}")
