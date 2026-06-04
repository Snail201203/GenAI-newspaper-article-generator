import os
from dotenv import load_dotenv
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import google.generativeai as genai

load_dotenv()

# --- Configure Gemini ---
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# --- Wikipedia Retrieval ---
def retrieve_from_wikipedia(topic: str) -> str:
    wiki = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=3000)
    tool = WikipediaQueryRun(api_wrapper=wiki)
    return tool.run(topic)

# --- RAG Pipeline ---
def generate_article(topic: str) -> dict:
    # Step 1: Retrieve context from Wikipedia (RAG - Retrieval step)
    print(f"Retrieving Wikipedia context for: {topic}")
    context = retrieve_from_wikipedia(topic)
    print(f"Context retrieved: {len(context)} characters")

    # Step 2: Augment prompt with context (RAG - Augmentation step)
    prompt = f"""
You are a professional newspaper journalist.

Using ONLY the context below, write a newspaper article about: {topic}

Context:
{context}

Your article must have:
- A catchy, engaging headline (prefix it with HEADLINE:)
- Exactly 3 paragraphs
- A neutral, journalistic tone
- Be concise and informative

Article:
"""

    # Step 3: Generate article (RAG - Generation step)
    print("Sending to Gemini...")
    response = model.generate_content(prompt)
    full_text = response.text
    print("Response received!")

    # Step 4: Parse headline and body
    if "HEADLINE:" in full_text:
        parts = full_text.split("HEADLINE:", 1)
        lines = parts[1].strip().split("\n", 1)
        headline = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""
    else:
        headline = "Generated Article"
        body = full_text

    return {"headline": headline, "body": body, "context": context}