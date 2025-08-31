import asyncio
from crawl4ai import AsyncWebCrawler, LLMExtractionStrategy, LLMConfig
from pydantic import BaseModel
from typing import List

# ✅ Define schema for structured extraction
class JobPosting(BaseModel):
    title: str = ""
    company: str = ""
    location: str = ""
    date_posted: str  = ""
    description: str = ""

class JobPostingsSchema(BaseModel):
    jobs: List[JobPosting]

async def main():
    # ✅ Explicitly define LLMConfig with provider and API token
    llm_cfg = LLMConfig(
        provider="gemini/gemini-1.5-flash", # Ensure this model is available to your API key
        api_token="AIzaSyCCVq-XWYG8TST16dcEoz_5U2qA6FkNDL4" # Replace with your actual Gemini API key
    )
    print("Loaded API token:", llm_cfg.api_token)  # Should not be None or empty

    # ✅ Create extraction strategy
    strategy = LLMExtractionStrategy(
        #schema=JobPostingsSchema.model_json_schema(),
        llm_config=llm_cfg
    )

    # ✅ Crawl the careers page
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://realpython.github.io/fake-jobs/",
            extraction_strategy=strategy
        )
        print(vars(result))
        print("Crawler success:", result.success)
        print("Error:", result.error_message)
        print("Crawled HTML length:", len(result.cleaned_html or ""))
        print("Preview:", (result.cleaned_html or "")[:500])  
        print("Raw LLM response:", getattr(result, "llm_response", None))
        print("Raw extracted_content:", result.extracted_content)

        print("Raw LLM response:", getattr(result, "llm_response", None))
        print("Raw extracted_content:", result.extracted_content)

        # ✅ Print extracted jobs
        if result.success and result.extracted_content:
            print("\n📌 Extracted Job Postings:\n")
            data = result.extracted_content
            jobs = data.get("jobs", data)  # supports dict or listcd 
            for job in jobs:
                print(f"- {job['title']} @ {job['company']} ({job['location']})")
        else:
            print("❌ Extraction failed:", result.error_message)


asyncio.run(main())