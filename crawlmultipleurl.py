import asyncio
from crawl4ai import AsyncWebCrawler

# List of URLs to crawl
urls = [
    "https://example.com",
    "https://www.python.org",
    "https://docs.crawl4ai.com"
]

async def crawl_multiple():
    # Initialize the crawler
    async with AsyncWebCrawler(verbose=True) as crawler:
        results = []

        for url in urls:
            try:
                # Crawl each URL
                result = await crawler.arun(url=url)
                print(f"\n✅ Crawled: {url}")
                print("Title:", result.markdown[:100], "...\n")  # preview first 100 chars

                results.append({
                    "url": url,
                    "content": result.markdown
                })
            except Exception as e:
                print(f"❌ Failed to crawl {url}: {e}")

        return results

if __name__ == "__main__":
    # Run the async crawler
    asyncio.run(crawl_multiple())
