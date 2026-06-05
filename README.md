# GenAI-newspaper-article-generator
### A context-aware newspaper article generator built with RAG (Retrieval-Augmented Generation) and LangChain. Given any topic, the tool retrieves real information from Wikipedia and generates a structured article with a eye catching headline and three paragraphs.

## How to run
### 1. Clone the repository
```bash
git clone https://github.com/Snail201203/GenAI-newspaper-article-generator.git
cd GenAI-newspaper-article-generator
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install langchain langchain-google-genai langchain-community langchain-core wikipedia streamlit python-dotenv google-generativeai
```

### 4. Set up your API key
Create a `.env` file in the root directory:
```
GOOGLE_API_KEY=your_google_ai_studio_key_here
```
Get your free API key at [aistudio.google.com](https://aistudio.google.com)

### 5. Run the app
```bash
streamlit run app.py
```
---