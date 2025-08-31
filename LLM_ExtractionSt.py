import asyncio
import os
import json
from crawl4ai import (
    AsyncWebCrawler,
    CrawlerRunConfig,
    LLMExtractionStrategy,
    LLMConfig
)
from crawl4ai.async_configs import BrowserConfig
from pydantic import BaseModel, Field
from typing import List, Optional


class OpenAIModelFee(BaseModel):
    model_name: str
    input_fee: Optional[str] = None
    output_fee: Optional[str] = None


class OpenAIModelFeeList(BaseModel):
    models: List[OpenAIModelFee]


async def main():
    browser_config = BrowserConfig(headless=True, verbose=True)

    run_config = CrawlerRunConfig(
        word_count_threshold=1,
        wait_for=5.0   # ✅ wait 5 seconds for JS to load
        # OR wait_for="table"  # ✅ wait until a <table> appears
    )

    llm_cfg = LLMConfig(
        provider="openai/gpt-4o-mini",
        api_token=os.getenv("API KEY"),
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://openai.com/api/pricing/",
            config=run_config,
            extraction_strategy=LLMExtractionStrategy(
                llm_config=llm_cfg,
                schema=OpenAIModelFeeList.schema(),
                extraction_type="json",
                instruction="""
                Extract OpenAI model names with their input and output fees.
                Example format:
                {
                  "models": [
                    {"model_name": "gpt-3.5", "input_fee": "$50", "output_fee": "$100"}
                  ]
                }
                """
            ),
        )

        print("----- RAW SCRAPED CONTENT (first 1200 chars) -----")
        print(result.markdown[:1200] if result.markdown else "⚠️ No text captured")

        print("\n----- EXTRACTION OUTPUT -----")
        if result.extracted_content:
            try:
                data = json.loads(result.extracted_content)
                print(json.dumps(data, indent=2))
            except json.JSONDecodeError:
                print("⚠️ Extracted content not valid JSON:")
                print(result.extracted_content)
        else:
            print("⚠️ No extracted content returned")


if __name__ == "__main__":
    asyncio.run(main())
