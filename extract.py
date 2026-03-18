"""
Parallel Extract API module for converting URLs to clean markdown content.
"""
from parallel import Parallel
from config import PARALLEL_API_KEY


def create_client() -> Parallel:
    """Create and return a Parallel client instance."""
    return Parallel(api_key=PARALLEL_API_KEY)


def extract(
    urls: list[str],
    objective: str | None = None,
    excerpts: bool = True,
    full_content: bool = False,
) -> dict:
    """
    Extract content from URLs using the Parallel Extract API.
    
    Args:
        urls: List of URLs to extract content from
        objective: Optional objective to focus excerpts on specific information
        excerpts: Whether to return focused excerpts (default True)
        full_content: Whether to return full page content as markdown
    
    Returns:
        Dictionary with extraction results containing titles, excerpts, and content
    """
    client = create_client()
    
    response = client.beta.extract(
        urls=urls,
        objective=objective,
        excerpts=excerpts,
        full_content=full_content,
    )
    
    results = []
    for result in response.results:
        results.append({
            "url": result.url,
            "title": result.title,
            "publish_date": result.publish_date,
            "excerpts": result.excerpts if excerpts else None,
            "full_content": result.full_content if full_content else None,
        })
    
    return {
        "extract_id": response.extract_id,
        "results": results,
        "result_count": len(results),
        "errors": [str(e) for e in response.errors] if response.errors else [],
    }


def extract_url(url: str, objective: str | None = None) -> dict:
    """
    Extract content from a single URL.
    
    Args:
        url: URL to extract content from
        objective: Optional objective to focus the extraction
    
    Returns:
        Dictionary with extraction result
    """
    result = extract(
        urls=[url],
        objective=objective,
        excerpts=True,
        full_content=False,
    )
    
    if result['results']:
        return result['results'][0]
    return {"url": url, "error": "No content extracted"}


def extract_full_page(url: str) -> dict:
    """
    Extract full page content as markdown from a URL.
    
    Args:
        url: URL to extract full content from
    
    Returns:
        Dictionary with full page content
    """
    result = extract(
        urls=[url],
        objective=None,
        excerpts=False,
        full_content=True,
    )
    
    if result['results']:
        return result['results'][0]
    return {"url": url, "error": "No content extracted"}


if __name__ == "__main__":
    print("Testing Parallel Extract API...")
    
    test_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    
    print(f"\n1. Extracting excerpts from: {test_url}")
    result = extract_url(test_url, objective="What is Python and who created it?")
    
    print(f"Title: {result.get('title', 'N/A')}")
    if result.get('excerpts'):
        print(f"Excerpt preview: {result['excerpts'][0][:300]}...")
    
    print("\n2. Testing multiple URL extraction...")
    multi_result = extract(
        urls=[
            "https://www.python.org/",
            "https://docs.python.org/3/tutorial/",
        ],
        objective="Python programming basics",
    )
    
    print(f"Extract ID: {multi_result['extract_id']}")
    print(f"URLs processed: {multi_result['result_count']}")
    for r in multi_result['results']:
        print(f"  - {r['title']}: {r['url']}")
