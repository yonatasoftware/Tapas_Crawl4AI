import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def main():
    strategy = JsonCssExtractionStrategy({
        "baseSelector": "div.gs-c-promo",
        "fields": [
            {"name": "title", "selector": "a.gs-c-promo-heading", "type": "text"},
            {"name": "url", "selector": "a.gs-c-promo-heading", "type": "attribute", "attribute": "href"}
        ]
    })

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www.bbc.com/news",
            extraction_strategy=strategy,
            use_browser=True,
            wait_for="a.gs-c-promo-heading",
            wait_for_timeout=10000,
            headers=headers   # ✅ pretend to be a real Chrome browser
        )

        if result.extracted_content:
            for item in result.extracted_content[:10]:
                print(item)
        else:
            print("⚠️ BBC still blocking. Let's test on quotes.toscrape.com instead.")

if __name__ == "__main__":
    asyncio.run(main())
