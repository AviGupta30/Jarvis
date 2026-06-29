"""
research_pipeline.py — End-to-End Autonomous Research Orchestrator
==================================================================
Chains the ResearchScraper and NLPExtractor to fetch live data
and integrate it into the Jarvis PPT engine.
"""
from app.services.research_scraper import ResearchScraper
from app.services.nlp_extractor import NLPExtractor
import json

def research_topic(topic: str):
    """
    Scrapes the web for a topic and extracts verified facts and statistics.
    Yields progress strings, then returns the final dictionary.
    """
    yield f"🔍 Researching live web for: '{topic}'...\n"
    
    scraper = ResearchScraper()
    sources = scraper.scrape_topic(topic, max_sources=4)
    
    if not sources:
        yield "⚠️ Could not fetch live web data. Falling back to internal knowledge.\n"
        return None
        
    yield f"🌐 Scraped {len(sources)} reliable sources. Extracting hard facts...\n"
    
    extractor = NLPExtractor()
    research_data = extractor.extract_facts(topic, sources)
    
    num_facts = len(research_data.get("verified_facts", []))
    num_stats = len(research_data.get("statistics", []))
    
    yield f"📈 Extracted {num_facts} verified facts and {num_stats} key statistics.\n"
    
    # Attach source URLs for provenance
    research_data["sources"] = [s["url"] for s in sources]
    return research_data
