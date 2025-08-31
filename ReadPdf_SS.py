url = "https://en.wikipedia.org/wiki/Mughal_Empire"
import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode
from base64 import b64decode

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            cache_mode=CacheMode.BYPASS,
            capture={"screenshot": True, "pdf": True}  # ✅ use capture
        )

    print("Success:", result.success)
    print("Has Screenshot:", bool(result.screenshot))
    print("Has PDF:", bool(result.pdf))

    if result.success:
        if result.screenshot:
            with open("screenshot.png", "wb") as f:
                f.write(b64decode(result.screenshot))

        if result.pdf:
            with open("document.pdf", "wb") as pdf_file:
                try:
                    pdf_file.write(b64decode(result.pdf))
                except Exception:
                    pdf_file.write(result.pdf)

if __name__ == "__main__":
    asyncio.run(main())
