import streamlit as st
from rag_pipeline import generate_article

# --- Page Config ---
st.set_page_config(
    page_title="GenAI Newspaper Article Generator",
    layout="centered"
)

# --- Header ---
st.title("Newspaper Article Generator")
st.markdown("*Powered by LangChain, Wikipedia RAG & Google Gemini*")
st.divider()

# --- Input ---
topic = st.text_input(
    "What topic do you want to generate an article about?",
    placeholder="e.g. Famous singers in Germany, Machine Learning, Dark series,...etc"
)

# --- Generate Button ---
if st.button("Generate Article", type="primary"):
    if not topic.strip():
        st.warning("Please enter the topic you want first.")
    else:
        with st.spinner("Searching Wikipedia and generating the article..."):
            try:
                result = generate_article(topic)
                
                # --- Display Article ---
                st.success("Article generated!")
                st.divider()
                
                # Headline
                st.markdown(f"## {result['headline']}")
                
                # Body
                st.markdown(result["body"])
                
                st.divider()
                
                # Show source context (collapsed)
                with st.expander("Source context from Wikipedia"):
                    st.write(result["context"])
                    
            except Exception as e:
                st.error(f"Something went wrong: {e}")

