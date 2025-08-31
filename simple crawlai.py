import nest_asyncio
nest_asyncio.apply()

import asyncio
import json
from crawl4ai import AsyncWebCrawler, LLMConfig
from pydantic import BaseModel
from typing import List

# Define schema for a simple knowledge graph (entities and relationships)
class Entity(BaseModel):
    name: str
    type: str

class Relationship(BaseModel):
    source: str
    target: str
    relation: str

class KnowledgeGraph(BaseModel):
    entities: List[Entity]
    relationships: List[Relationship]

def make_serializable(obj):
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items() if not callable(v)}
    elif isinstance(obj, list):
        return [make_serializable(i) for i in obj if not callable(i)]
    elif isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    else:
        return str(obj)  # Fallback: convert unknown types to string

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://thekidsbestclinic.com")
        #print("Raw result.json:", result.json)  # Debug print
        serializable_json = make_serializable(result.json)
        json_str = json.dumps(serializable_json, indent=2)
        print(json_str)  # This is the input you can feed to your LLM

asyncio.run(main())