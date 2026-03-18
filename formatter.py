import json
from typing import Literal
from datetime import datetime
from search import SearchResponse, SearchResult


class ResultFormatter:
    """Format search results in various output formats."""
    
    @staticmethod
    def to_json(response: SearchResponse, pretty: bool = True) -> str:
        """Convert search response to JSON string."""
        data = {
            "search_id": response.search_id,
            "query": response.query,
            "objective": response.objective,
            "result_count": len(response.results),
            "results": [
                {
                    "url": r.url,
                    "title": r.title,
                    "excerpts": r.excerpts,
                    "publish_date": r.publish_date
                }
                for r in response.results
            ]
        }
        if pretty:
            return json.dumps(data, indent=2)
        return json.dumps(data)
    
    @staticmethod
    def to_markdown(response: SearchResponse) -> str:
        """Convert search response to Markdown format."""
        lines = [
            f"# Search Results",
            f"",
            f"**Query:** {response.query}",
            f"**Objective:** {response.objective}",
            f"**Results Found:** {len(response.results)}",
            f"**Search ID:** `{response.search_id}`",
            f"",
            "---",
            ""
        ]
        
        for i, result in enumerate(response.results, 1):
            lines.append(f"## {i}. {result.title}")
            lines.append(f"")
            lines.append(f"**URL:** [{result.url}]({result.url})")
            if result.publish_date:
                lines.append(f"**Published:** {result.publish_date}")
            lines.append(f"")
            if result.excerpts:
                lines.append("### Excerpts")
                for excerpt in result.excerpts[:2]:
                    clean_excerpt = excerpt[:500] + "..." if len(excerpt) > 500 else excerpt
                    lines.append(f"> {clean_excerpt}")
                    lines.append("")
            lines.append("---")
            lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def to_text(response: SearchResponse) -> str:
        """Convert search response to plain text format."""
        lines = [
            "=" * 60,
            "SEARCH RESULTS",
            "=" * 60,
            f"Query: {response.query}",
            f"Objective: {response.objective}",
            f"Results: {len(response.results)}",
            "-" * 60,
            ""
        ]
        
        for i, result in enumerate(response.results, 1):
            lines.append(f"[{i}] {result.title}")
            lines.append(f"    URL: {result.url}")
            if result.publish_date:
                lines.append(f"    Date: {result.publish_date}")
            lines.append("")
        
        return "\n".join(lines)


class ResultExporter:
    """Export search results to files."""
    
    @staticmethod
    def export(
        response: SearchResponse,
        filepath: str,
        format: Literal["json", "markdown", "text"] = "json"
    ) -> str:
        """
        Export search results to a file.
        
        Args:
            response: The search response to export
            filepath: Path to save the file
            format: Output format (json, markdown, text)
            
        Returns:
            The filepath where results were saved
        """
        formatter = ResultFormatter()
        
        if format == "json":
            content = formatter.to_json(response)
        elif format == "markdown":
            content = formatter.to_markdown(response)
        else:
            content = formatter.to_text(response)
        
        with open(filepath, "w") as f:
            f.write(content)
        
        return filepath


if __name__ == "__main__":
    from search import ParallelSearch
    
    searcher = ParallelSearch(api_key="Bh5qbK7OhHVAl1NgDfyoT2oHjcA9DvHfyXQL8gp9")
    response = searcher.quick_search(
        query="AI trends 2026",
        objective="Find current AI industry trends",
        max_results=3
    )
    
    print("=== JSON Format ===")
    print(ResultFormatter.to_json(response)[:500] + "...")
    
    print("\n=== Text Format ===")
    print(ResultFormatter.to_text(response))
    
    print("\n=== Markdown Format (preview) ===")
    print(ResultFormatter.to_markdown(response)[:500] + "...")
    
    exported = ResultExporter.export(response, "test_export.json", "json")
    print(f"\nExported to: {exported}")
