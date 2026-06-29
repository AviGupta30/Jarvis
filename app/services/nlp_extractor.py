"""
nlp_extractor.py — LLM-Powered Fact & Entity Extractor
======================================================
Uses Groq to process scraped web text and extract verified facts, statistics,
and chart-ready data points to inject into the PPT generator.
"""
import os
import json
import re

from dotenv import load_dotenv
load_dotenv()

# Use Groq client from Jarvis if available, or initialize directly
try:
    from groq import Groq
    _GROQ = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    print(f"Error loading Groq: {e}")
    _GROQ = None

_SYS_EXTRACT = """\
You are an elite data extraction NLP engine.
Your job is to read raw web scraped text and extract concrete, verifiable facts, statistics, and entities.
Return ONLY valid JSON. No markdown fences. No explanations."""

_USR_EXTRACT = """\
TOPIC: {topic}
SOURCE URL: {url}
RAW TEXT:
{text}

Extract the most important facts, numbers, dates, and statistics related to the TOPIC.
If the text does not contain relevant facts, return empty lists.

JSON SCHEMA:
{{
  "verified_facts": [
    "A concise, verifiable fact string (e.g. 'Highest placement package was 82 LPA at Atlassian')",
    "Another fact..."
  ],
  "statistics": [
    {{"label": "Average Package", "value": "15 LPA"}},
    {{"label": "Companies Visited", "value": "400+"}}
  ]
}}"""

class NLPExtractor:
    def __init__(self):
        if _GROQ is None:
            raise RuntimeError("GROQ_API_KEY not found in environment.")

    def _parse(self, raw: str) -> dict:
        raw = re.sub(r"```(?:json)?|```", "", raw).strip()
        try:
            return json.loads(raw[raw.find("{"):raw.rfind("}") + 1])
        except Exception:
            return {"verified_facts": [], "statistics": []}

    def extract_facts(self, topic: str, scraped_sources: list[dict]) -> dict:
        """
        Runs extraction on each scraped source and aggregates the results.
        Returns a combined dictionary of facts and statistics.
        """
        all_facts = set()
        all_stats = {}

        for src in scraped_sources:
            url = src.get("url", "")
            text = src.get("text", "")
            if not text:
                continue

            try:
                r = _GROQ.chat.completions.create(
                    model="llama-3.1-8b-instant", # Fast model for extraction
                    messages=[
                        {"role": "system", "content": _SYS_EXTRACT},
                        {"role": "user", "content": _USR_EXTRACT.format(topic=topic, url=url, text=text)}
                    ],
                    max_tokens=1000,
                    temperature=0.1,
                    response_format={"type": "json_object"}
                )
                res = self._parse(r.choices[0].message.content or "")
                
                # Aggregate facts (deduplicate via set)
                for f in res.get("verified_facts", []):
                    all_facts.add(f)
                    
                # Aggregate stats (keep latest/highest if duplicate label?)
                # For simplicity, we just keep the first one found per label
                for stat in res.get("statistics", []):
                    label = stat.get("label", "").strip()
                    if label and label not in all_stats:
                        all_stats[label] = stat.get("value")

            except Exception as e:
                print(f"[NLPExtractor] Extraction failed for {url}: {e}")

        return {
            "verified_facts": list(all_facts)[:15], # Cap at top 15 facts
            "statistics": [{"label": k, "value": v} for k, v in list(all_stats.items())[:10]]
        }

if __name__ == "__main__":
    ext = NLPExtractor()
    print("NLPExtractor loaded successfully.")
