"""
Parallel Search API module for web searches with LLM-optimized excerpts.
"""
from parallel import Parallel
from config import PARALLEL_API_KEY


def create_client() -> Parallel:
    """Create and return a Parallel client instance."""
    return Parallel(api_key=PARALLEL_API_KEY)


def search(
    objective: str,
    search_queries: list[str],
    mode: str = "fast",
    max_results: int = 10,
    max_chars_per_result: int = 10000,
) -> dict:
    """
    Execute a web search using the Parallel Search API.
    
    Args:
        objective: Natural language description of what you're looking for
        search_queries: List of search queries to execute
        mode: Search mode - "fast", "one-shot", or "thorough"
        max_results: Maximum number of results to return
        max_chars_per_result: Maximum characters per result excerpt
    
    Returns:
        Dictionary with search results containing urls, titles, and excerpts
    """
    client = create_client()
    
    response = client.beta.search(
        objective=objective,
        search_queries=search_queries,
        mode=mode,
        max_results=max_results,
        excerpts={"max_chars_per_result": max_chars_per_result},
    )
    
    results = []
    for result in response.results:
        results.append({
            "url": result.url,
            "title": result.title,
            "publish_date": result.publish_date,
            "excerpts": result.excerpts,
        })
    
    return {
        "search_id": response.search_id,
        "results": results,
        "result_count": len(results),
    }


def quick_search(query: str, max_results: int = 5) -> dict:
    """
    Simplified search with a single query string.
    
    Args:
        query: Search query string
        max_results: Maximum number of results
    
    Returns:
        Dictionary with search results
    """
    return search(
        objective=query,
        search_queries=[query],
        mode="fast",
        max_results=max_results,
    )


if __name__ == "__main__":
    print("Testing Parallel Search API...")
    
    result = quick_search("What is the capital of France?", max_results=3)
    
    print(f"\nSearch ID: {result['search_id']}")
    print(f"Results found: {result['result_count']}")
    
    for i, r in enumerate(result['results'], 1):
        print(f"\n--- Result {i} ---")
        print(f"Title: {r['title']}")
        print(f"URL: {r['url']}")
        if r['excerpts']:
            print(f"Excerpt preview: {r['excerpts'][0][:200]}...")
