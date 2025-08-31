from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from base64 import b64decode
import asyncio

async def main():
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        screenshot=True,
        screenshot_wait_for=1.0,  # optional delay before capture
        pdf=True
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://en.wikipedia.org/wiki/Mughal_Empire",
            config=run_config
        )

    print("Success:", result.success)
    print("Has Screenshot:", bool(result.screenshot))
    print("Has PDF:", bool(result.pdf))

    if result.success:
        if result.screenshot:
            with open("screenshot.png", "wb") as f:
                f.write(b64decode(result.screenshot))
            print("Screenshot saved.")
        else:
            print("No screenshot returned.")

        if result.pdf:
            with open("document.pdf", "wb") as f:
                f.write(result.pdf)
            print("PDF saved.")
        else:
            print("No PDF returned.")

if __name__ == "__main__":
    asyncio.run(main())
