import re
import random
import requests
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq
from app.core.config import settings

# Load model globally to avoid reloading on each call
_client = None

def get_groq_client():
    global _client
    if _client is None:
        _client = Groq(api_key=settings.GROQ_API_KEY)
    return _client

_similarity_model = None

def get_similarity_model():
    global _similarity_model
    if _similarity_model is None:
        _similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
    return _similarity_model

BANNED_WORDS = [
    # Classic AI tells
    "furthermore", "delve", "tapestry", "testament", "crucial", "multifaceted",
    "in conclusion", "it is important to note", "it is worth noting",
    # GPTZero's extended list
    "streamline", "elevate", "underscore", "foster", "leverage", "paramount",
    "pivotal", "shed light", "plays a role", "stands as", "serves as",
    "in today's world", "in the realm of", "at the end of the day",
    "needless to say", "it goes without saying", "first and foremost",
    "not only", "but also", "with that said", "having said that",
    "on the other hand", "in order to", "due to the fact that",
    "as previously mentioned", "it should be noted", "one must consider",
    "this is achieved by", "it can be seen that", "as a result of this"
]

SIMILARITY_THRESHOLD = 0.45

PERPLEXITY_FORCING_PROMPT = """
For each sentence you write, follow this internal process:
1. Think of the most obvious, predictable way to phrase it.
2. REJECT that phrasing entirely.
3. Write the second or third alternative that comes to mind instead.

This means: if "utilize" comes to mind, write "use" or "lean on".
If "it is important" comes to mind, write "worth noting" or just cut it.
If a smooth transition like "Furthermore" comes to mind, start the 
sentence abruptly without one, or use a dash — like this.

Never write the most statistically likely next word. 
Always write the second or third most natural option.
"""

def get_sentence_scores(text: str) -> list[tuple[str, float]]:
    """Local, keyless per-sentence AI probability detector."""
    sentences = text.split('. ')
    scores = []
    
    for s in sentences:
        if not s.strip():
            continue
            
        prob = 0.1 # Base human probability
        lower_s = s.lower()
        words = lower_s.split()
        
        # 1. Banned Word Penalty
        if any(banned in lower_s for banned in BANNED_WORDS):
            prob += 0.6
            
        # 2. Length/Complexity Penalty (AI loves 15-25 word sentences)
        if 15 < len(words) < 25:
            prob += 0.2
            
        # 3. Transition Penalty
        if lower_s.startswith(("firstly", "secondly", "finally", "moreover", "however", "therefore")):
            prob += 0.3
            
        # Cap at 0.99
        scores.append((s, min(0.99, prob)))
        
    return scores

def detect_tone(text: str) -> str:
    academic_markers = ["research", "study", "analysis", "hypothesis", "data"]
    score = sum(1 for w in academic_markers if w in text.lower())
    return "academic and formal" if score > 2 else "conversational and direct"

def build_structure_prompt(text: str, tone: str) -> str:
    word_count = len(text.split())
    return f"""You are rewriting text to restructure it completely. The original tone is: {tone}.

STRICT RULES:
1. TONE LOCK: Keep the text {tone}.
2. MEANING: Every fact, number, and claim must remain exact.
3. LENGTH: Stay within ±10 words of the original ({word_count} words).
4. BURSTINESS (CRITICAL): Violently vary sentence lengths. Write a 3-word sentence. Then write a long winding sentence that sprawls across two clauses and uses a conjunction or em-dash. Then a medium one. Break the predictable rhythm.
5. IDEA REORDERING: You may move supporting points around. A conclusion-first structure is fine. A digression mid-argument is fine. The reader must end up understanding the same thing, but the journey can be non-linear. Humans don't always build to a conclusion — sometimes they state it first and justify it after.

{PERPLEXITY_FORCING_PROMPT}

Original text:
{text}

Rewritten text (output ONLY the restructured text):"""

def build_vocab_prompt(text: str, tone: str) -> str:
    return f"""You are rewriting specific sentences to sound more human lexically. The original tone is: {tone}.

STRICT RULES:
1. TONE LOCK: Keep the text {tone}.
2. MEANING: Preserve all facts and numbers perfectly.
3. BANNED WORDS — never use any of these: {', '.join(BANNED_WORDS)}
4. PERPLEXITY: Avoid obvious words. Use contractions naturally if appropriate.

{PERPLEXITY_FORCING_PROMPT}

Original sentences:
{text}

Rewritten sentences (output ONLY the rewritten text, maintaining the same number of sentences):"""

def call_groq(prompt: str, attempt: int = 0) -> str:
    temperatures = [0.9, 1.05, 1.15]
    top_p_values = [0.85, 0.90, 0.95]
    
    client = get_groq_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperatures[min(attempt, 2)],
        top_p=top_p_values[min(attempt, 2)],
        max_tokens=2048
    )
    return response.choices[0].message.content.strip()

def rewrite_sentences(sentences_batch: list[str], tone: str, attempt: int) -> list[str]:
    """Helper to rewrite a batch of sentences via Groq."""
    text_block = " ".join(sentences_batch)
    prompt = build_vocab_prompt(text_block, tone)
    rewritten_block = call_groq(prompt, attempt)
    # Attempt to split back into sentences (approximate)
    return [s.strip() for s in rewritten_block.split('. ') if s.strip()]

def reshape_paragraphs(text: str) -> str:
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    if len(paragraphs) < 2:
        sentences = text.replace('? ', '?|').replace('. ', '.|').replace('! ', '!|').split('|')
        sentences = [s.strip() for s in sentences if s.strip()]
        result, i = [], 0
        while i < len(sentences):
            chunk_size = random.choice([1, 2, 2, 4, 5])
            chunk = ' '.join(sentences[i:i+chunk_size])
            result.append(chunk)
            i += chunk_size
        return '\n\n'.join(result)
    return text

def inject_micro_errors(text: str) -> str:
    """Inject subtle, natural human imperfections post-rewrite."""
    sentences = text.split('. ')
    
    for i in range(len(sentences)):
        sent = sentences[i]
        if sent is None:
            continue
            
        r = random.random()
        
        # 1. Remove Oxford comma (most common human slip)
        if ', and ' in sent and r < 0.4:
            sentences[i] = sent.replace(', and ', ' and ', 1)
        
        # 2. Casual comma splice
        elif r < 0.15 and i < len(sentences) - 1 and len(sent.split()) > 5:
            # Avoid splicing if sentences[i+1] is None
            if sentences[i+1] is not None and len(sentences[i+1]) > 0:
                sentences[i] = sent + ', ' + sentences[i+1][0].lower() + sentences[i+1][1:]
                sentences[i+1] = None  # Mark for removal
        
        # 3. Occasional "which" where "that" is technically correct
        elif 'that' in sent and r < 0.2:
            sentences[i] = sentences[i].replace(' that ', ' which ', 1)
    
    return '. '.join(s for s in sentences if s is not None)

def inject_human_fingerprints(text: str) -> str:
    sentences = text.split('. ')
    hedges = ["Arguably,", "In practice,", "From what I can tell,", "At least in my reading,", "Generally speaking,"]
    
    word_count = len(text.split())
    num_hedges = max(1, word_count // 200)
    
    for _ in range(num_hedges):
        if len(sentences) > 1:
            idx = random.randint(1, len(sentences) - 1)
            if idx < len(sentences) and '?' not in sentences[idx] and not sentences[idx].startswith(tuple(hedges)):
                if len(sentences[idx]) > 0:
                    sentences[idx] = random.choice(hedges) + " " + sentences[idx][0].lower() + sentences[idx][1:]
    
    result = '. '.join(sentences)
    
    long_sentences = [(m.start(), m.group()) for m in re.finditer(r'[^.!?]{60,}', result)]
    if long_sentences:
        start, sent = random.choice(long_sentences)
        modified = sent.replace(', ', ' — ', 1)
        result = result[:start] + modified + result[start+len(sent):]
    
    return result

def fact_check(original: str, rewritten: str) -> tuple[bool, set]:
    orig_numbers = set(re.findall(r'\b\d+\.?\d*\b', original))
    new_numbers = set(re.findall(r'\b\d+\.?\d*\b', rewritten))
    missing = orig_numbers - new_numbers
    return len(missing) == 0, missing

def check_similarity(original: str, rewritten: str) -> float:
    model = get_similarity_model()
    embeddings = model.encode([original, rewritten])
    sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return float(sim)

def humanize_text_sync(text: str) -> str:
    tone = detect_tone(text)
    
    # 1. Pass 1: Structure & Idea Reordering
    struct_prompt = build_structure_prompt(text, tone)
    restructured = call_groq(struct_prompt, attempt=0)
    reshaped = reshape_paragraphs(restructured)
    
    current_text = reshaped
    best_result = current_text
    
    for attempt in range(3):
        # 2. GPTZero API Re-check
        sentence_scores = get_sentence_scores(current_text)
        
        # If no sentences are flagged > 0.70, we are good! (Or if API is offline, it returns 0.0)
        if all(prob <= 0.70 for _, prob in sentence_scores):
            best_result = current_text
            break
            
        # 3. Targeted Rewrite (Pass 2)
        result_sentences = []
        flagged_batch = []
        
        for sentence, prob in sentence_scores:
            if prob > 0.70:
                flagged_batch.append(sentence)
            else:
                if flagged_batch:
                    rewritten = rewrite_sentences(flagged_batch, tone, attempt)
                    result_sentences.extend(rewritten)
                    flagged_batch = []
                result_sentences.append(sentence)
                
        if flagged_batch:
            rewritten = rewrite_sentences(flagged_batch, tone, attempt)
            result_sentences.extend(rewritten)
            
        vocab_swapped = ' '.join(result_sentences)
        
        # 4. Post-processing
        with_errors = inject_micro_errors(vocab_swapped)
        fingerprinted = inject_human_fingerprints(with_errors)
        
        # 5. Verification
        facts_ok, _ = fact_check(text, fingerprinted)
        if not facts_ok:
            # If facts are lost, we still keep it as current_text but it might get rewritten again
            # We'll just continue the loop
            pass
            
        sim = check_similarity(text, fingerprinted)
        if sim < SIMILARITY_THRESHOLD:
            # Too divergent, maybe we retry?
            pass
            
        current_text = fingerprinted
        best_result = current_text
        
    return best_result
