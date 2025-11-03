import streamlit as st
import os

# App configuration
st.set_page_config(
    page_title="Chat App",
    page_icon="💬",
    layout="wide"
)

# Main app
st.title("💬 Chat App Coming Soon!")
st.write("This is a placeholder Streamlit app.")

# Display environment info (for debugging)
if st.checkbox("Show Environment Info"):
    st.write("**Environment Variables:**")
    st.write(f"- Database: {os.getenv('POSTGRES_DB', 'Not set')}")
    st.write(f"- LightRAG URL: {os.getenv('LIGHTRAG_URL', 'Not set')}")
    st.write(f"- Server Port: {os.getenv('STREAMLIT_SERVER_PORT', 'Not set')}")
