import os
import json
import requests
import google.generativeai as genai
from typing import Union

def build_prompt(idea: str, platform: str, tone: str, creativity: float, formality: float, 
                 smart_emojis: bool, auto_hashtag: bool, contextual_suggestions: bool, 
                 target_audience: str = "", original_content: dict = None, refinement_instruction: str = "") -> str:
    
    if creativity <= 33: creativity_level = "safe"
    elif creativity <= 66: creativity_level = "balanced"
    else: creativity_level = "inventive"
        
    if formality <= 33: formality_level = "very casual"
    elif formality <= 66: formality_level = "neutral"
    else: formality_level = "very formal"

    platform_specific_instruction = ""
    if platform.lower() == "x" or platform.lower() == "twitter":
        platform_specific_instruction = "- Critical: Ensure each tweet in the thread is under 280 characters."

    if platform.lower() == "instagram": 
        content_structure = '"content": {"caption": "Your generated caption.", "script": "A short video script."}'
    elif platform.lower() in ["x", "twitter"]: 
        content_structure = '"content": {"thread": ["Tweet 1.", "Tweet 2."]}'
    else: 
        content_structure = '"content": "Your full generated text post."'

    base_prompt = f"""
    You are an expert social media content creator. Generate content and analysis based on these specs:
    - Idea: "{idea}"
    - Platform: {platform}
    {'- Target Audience: ' + target_audience if target_audience else ''}
    {platform_specific_instruction}
    - Tone: "{tone}"
    - Formality: {formality_level}
    - Creativity: {creativity_level}
    {'- Add smart emojis.' if smart_emojis else ''}
    {'- Add relevant hashtags.' if auto_hashtag else ''}
    {'- Add a suggestion.' if contextual_suggestions else ''}

    Your entire response must be a single, valid JSON object with "content" and "analysis" keys.
    The "content" key's value must follow this structure: {{{content_structure}}}.
    
    The "analysis" key must contain a JSON object with three integer scores. CRITICAL: Generate scores on a human-like scale where 75 is average, 85 is good, and 95 is excellent. Do not give unusually low scores unless the content is extremely flawed. The keys must be exactly: "readability", "engagement_potential", and "human_likeness".
    
    Do not include any other text or markdown.
    """

    if original_content and refinement_instruction:
        original_content_json = json.dumps(original_content)
        return f"""
        {base_prompt}

        You are now REFINING the following content based on a user's instruction.
        ---
        ORIGINAL CONTENT:
        {original_content_json}
        ---
        USER'S REFINEMENT INSTRUCTION: "{refinement_instruction}"
        ---
        Apply the instruction to the original content and provide the new, refined content and its new analysis in the required JSON format.
        """
    return base_prompt


def call_llm(prompt: str) -> str:
    """Calls Groq Llama 3.3 70B directly for maximum speed. No slow fallbacks."""
    from groq import Groq
    from app.core.config import settings
    
    client = Groq(api_key=settings.GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

def generate_social_content(idea: str, platform: str = "Instagram", tone: str = "engaging", 
                            creativity: float = 50.0, formality: float = 50.0, 
                            smart_emojis: bool = True, auto_hashtag: bool = True, 
                            contextual_suggestions: bool = True, target_audience: str = "") -> str:
    """
    Generate professional, multi-version social media content.
    """
    prompt = build_prompt(idea, platform, tone, creativity, formality, smart_emojis, auto_hashtag, contextual_suggestions, target_audience)
    
    versions = []
    import concurrent.futures
    
    approaches = [
        "Focus on an engaging hook and a storytelling approach.",
        "Focus on direct value, punchy sentences, and bold statements.",
        "Focus on being relatable, conversational, and asking a question to the audience."
    ]
    
    # Generate 3 unique versions in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(call_llm, prompt + f"\n\nCRITICAL APPROACH: {approaches[i]}") for i in range(3)]
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                json_str = result.strip().replace("```json", "").replace("```", "")
                data = json.loads(json_str)
                versions.append(data)
            except Exception as e:
                print(f"[ContentManager] Failed to generate version: {e}")
            
    if not versions:
        return "Failed to generate social content. Please check API keys and internet connection."

    # Performance Prediction Analysis
    try:
        content_to_analyze = ""
        for i, v in enumerate(versions):
            content_to_analyze += f"--- VERSION {i+1} ---\n{json.dumps(v.get('content', ''))}\n\n"
            
        prediction_prompt = f"""You are a viral social media strategist. Analyze the following {len(versions)} content options for a {platform} post. For each, provide a "virality_score" (0-100) and a brief "justification". Your response must be ONLY a valid JSON list of objects. Example: [{{"version_index": 0, "virality_score": 88, "justification": "Strong hook."}}] \n\nContent to analyze:\n{content_to_analyze}"""
        
        pred_result = call_llm(prediction_prompt)
        pred_json = json.loads(pred_result.strip().replace("```json", "").replace("```", ""))
        
        for prediction in pred_json:
            idx = prediction.get("version_index")
            if idx is not None and 0 <= idx < len(versions):
                versions[idx]["virality_score"] = prediction.get("virality_score")
                versions[idx]["justification"] = prediction.get("justification")
    except Exception as e:
        print(f"[ContentManager] Performance prediction failed: {e}")

    # Format the output into a readable string for Jarvis
    output = f"Generated {len(versions)} versions for {platform}:\n\n"
    for i, v in enumerate(versions):
        output += f"--- Version {i+1} ---\n"
        content = v.get("content", {})
        if isinstance(content, dict):
            for k, val in content.items():
                if isinstance(val, list):
                    output += f"{k.capitalize()}:\n" + "\n".join(f"- {item}" for item in val) + "\n"
                else:
                    output += f"{k.capitalize()}: {val}\n"
        else:
            output += f"Content: {content}\n"
            
        analysis = v.get("analysis", {})
        output += f"\nScores: Readability: {analysis.get('readability')}, Engagement: {analysis.get('engagement_potential')}, Human Likeness: {analysis.get('human_likeness')}\n"
        if "virality_score" in v:
            output += f"Virality Score: {v.get('virality_score')} - {v.get('justification')}\n"
        output += "\n"
        
    return output


def refine_social_content(original_content: str, refinement_instruction: str, platform: str = "Instagram") -> str:
    """
    Refine an existing piece of social media content based on user instructions.
    original_content can be a copy-pasted version from the generation tool.
    """
    # Create a dummy dict to represent original content
    orig_dict = {"content": original_content}
    prompt = build_prompt(idea="Refinement", platform=platform, tone="adaptive", creativity=50, formality=50, 
                          smart_emojis=True, auto_hashtag=True, contextual_suggestions=False,
                          original_content=orig_dict, refinement_instruction=refinement_instruction)
                          
    try:
        result = call_llm(prompt)
        json_str = result.strip().replace("```json", "").replace("```", "")
        data = json.loads(json_str)
        
        output = f"--- Refined Version ({platform}) ---\n"
        content = data.get("content", {})
        if isinstance(content, dict):
            for k, val in content.items():
                if isinstance(val, list):
                    output += f"{k.capitalize()}:\n" + "\n".join(f"- {item}" for item in val) + "\n"
                else:
                    output += f"{k.capitalize()}: {val}\n"
        else:
            output += f"Content: {content}\n"
            
        analysis = data.get("analysis", {})
        output += f"\nScores: Readability: {analysis.get('readability')}, Engagement: {analysis.get('engagement_potential')}, Human Likeness: {analysis.get('human_likeness')}\n"
        
        return output
    except Exception as e:
        return f"Failed to refine content: {e}"
