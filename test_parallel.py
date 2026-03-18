from parallel import Parallel

client = Parallel(api_key="Bh5qbK7OhHVAl1NgDfyoT2oHjcA9DvHfyXQL8gp9")
response = client.beta.search(
    mode="one-shot",
    search_queries=["NVIDIA AI market cap impact"],
    max_results=10,
    objective="Analysis of the impact of AI on NVIDIA's increased market cap",
)
print(response)
