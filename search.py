from typing import List, Optional, Literal
from dataclasses import dataclass
from parallel_client import ParallelClient


@dataclass
class SearchResult:
    """Represents a single search result."""
    url: str
    title: str
    excerpts: List[str]
    publish_date: Optional[str] = None


@dataclass
class SearchResponse:
    """Represents the complete search response."""
    results: List[SearchResult]
    search_id: str
    query: str
    objective: str


class ParallelSearch:
    """Search functionality using the Parallel API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with optional API key."""
        self._client = ParallelClient(api_key=api_key)
    
    def search(
        self,
        queries: List[str],
        objective: str,
        mode: Literal["one-shot", "iterative"] = "one-shot",
        max_results: int = 10
    ) -> SearchResponse:
        """
        Perform a search using the Parallel API.
        
        Args:
            queries: List of search queries to execute
            objective: The goal/context for the search
            mode: Search mode - "one-shot" for quick results, "iterative" for deeper search
            max_results: Maximum number of results to return
            
        Returns:
            SearchResponse with parsed results
        """
        response = self._client.client.beta.search(
            mode=mode,
            search_queries=queries,
            max_results=max_results,
            objective=objective,
        )
        
        results = []
        for item in response.results:
            results.append(SearchResult(
                url=item.url,
                title=item.title,
                excerpts=item.excerpts,
                publish_date=getattr(item, 'publish_date', None)
            ))
        
        return SearchResponse(
            results=results,
            search_id=response.search_id,
            query=", ".join(queries),
            objective=objective
        )
    
    def quick_search(self, query: str, objective: str, max_results: int = 5) -> SearchResponse:
        """Convenience method for a single quick search."""
        return self.search(
            queries=[query],
            objective=objective,
            mode="one-shot",
            max_results=max_results
        )


if __name__ == "__main__":
    searcher = ParallelSearch(api_key="Bh5qbK7OhHVAl1NgDfyoT2oHjcA9DvHfyXQL8gp9")
    
    print("Testing quick_search...")
    response = searcher.quick_search(
        query="Python best practices 2026",
        objective="Find current Python coding best practices",
        max_results=3
    )
    
    print(f"\nSearch ID: {response.search_id}")
    print(f"Query: {response.query}")
    print(f"Results found: {len(response.results)}")
    
    for i, result in enumerate(response.results, 1):
        print(f"\n--- Result {i} ---")
        print(f"Title: {result.title}")
        print(f"URL: {result.url}")
        print(f"Date: {result.publish_date}")
