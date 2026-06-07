"""
skill_prompt_enhancer.py
━━━━━━━━━━━━━━━━━━━━━━━━
Jarvis feature: Prompt enhancement core capability.
Phase 1: Just the Groq API call to refine prompts.
"""

from groq import Groq
from app.core.config import settings
from app.services.prompt_enhancement_library import detect_domain, get_system_prompt, validate_enhancement

def enhance_prompt(raw_prompt: str) -> str:
    """
    Takes a raw user prompt and converts it into a masterfully crafted, 
    high-performance prompt using Llama 3.1 70B via Groq.
    """
    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        domain = detect_domain(raw_prompt)
        system_prompt = get_system_prompt(domain)
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": raw_prompt}
            ],
            temperature=0.3,  # Deterministic, structured enhancement
            max_tokens=800,
        )
        
        enhanced = response.choices[0].message.content.strip()
        
        # Validation pass
        clean, issues = validate_enhancement(raw_prompt, enhanced)
        if issues:
            print("[Enhancer Warnings]:", issues)
            
        return f"**ENHANCED PROMPT ({domain.upper()})**:\n\n{clean}"
    except Exception as e:
        return f"Failed to enhance prompt: {e}"

def enhance_and_respond(raw_prompt: str) -> str:
    """
    Two-stage pipeline:
    1. Enhance the prompt.
    2. Get the answer using the enhanced prompt.
    """
    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        domain = detect_domain(raw_prompt)
        system_prompt = get_system_prompt(domain)
        
        # Stage 1: Enhance
        enhancement_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": raw_prompt}
            ],
            temperature=0.3,
            max_tokens=800,
        )
        enhanced_prompt = enhancement_response.choices[0].message.content.strip()
        
        clean, issues = validate_enhancement(raw_prompt, enhanced_prompt)
        if issues:
            print("[Enhancer Warnings]:", issues)
        
        enhanced_prompt = clean
        
        # Stage 2: Respond
        final_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": enhanced_prompt}
            ],
            temperature=0.7,
            max_tokens=2048,
        )
        
        answer = final_response.choices[0].message.content.strip()
        return f"ENHANCED PROMPT:\n{enhanced_prompt}\n\n---\n\nANSWER:\n{answer}"
    except Exception as e:
        return f"Failed to enhance and respond: {e}"
