import os
from click import prompt
from dotenv import load_dotenv
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import google.generativeai as genai

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# Wikipedia Retrieval
def retrieve_from_wikipedia(topic: str) -> str:
    wiki = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=3000)
    tool = WikipediaQueryRun(api_wrapper=wiki)
    return tool.run(topic)

# RAG 
def generate_article(topic: str) -> dict:
    # Retrieve context from Wikipedia 
    print(f"Retrieving Wikipedia context for: {topic}")
    context = retrieve_from_wikipedia(topic)
    print(f"Context retrieved: {len(context)} characters")

    # Augment prompt with context 
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

    # Generate the article 
    print("Sending to Gemini...")
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
        temperature=0.7,
        max_output_tokens=1000,
    )
    )

     # Safety check
    if not response.candidates:
        raise ValueError("Gemini returned no candidates — topic may have been blocked by safety filters")

    full_text = response.text
    print("Response received!")

    #Parse headline and body
    if "HEADLINE:" in full_text:
        parts = full_text.split("HEADLINE:", 1)
        lines = parts[1].strip().split("\n", 1)
        headline = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""
    else:
        headline = "Generated Article"
        body = full_text

    return {"headline": headline, "body": body, "context": context}