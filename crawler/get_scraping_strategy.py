# get_scraping_strategy.py

import re
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai.content_scraping_strategy import WebScrapingStrategy
from .strategies.cnki_strategy import CNKIScrapingStrategy

def get_scraping_strategy(url: str, llm_extractor: LLMExtractionStrategy) -> WebScrapingStrategy:

    is_cnki = re.search(r"(cnki\.net|cnki\.com\.cn)", url, re.IGNORECASE) is not None
    if is_cnki:
        return CNKIScrapingStrategy(llm_extractor)
    else:
        strategy = WebScrapingStrategy()
        strategy.extraction_strategy = llm_extractor
        return strategy
