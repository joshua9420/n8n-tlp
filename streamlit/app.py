"""
Main Chat Hub Application
"""
import streamlit as st
from config import settings
from auth import auth

# Page configuration
st.set_page_config(
    page_title="Chat Hub",
    page_icon="�",
    layout="wide"
)

# Require authentication
auth.require_auth()

# Main content (only shown to authenticated users)
if auth.is_authenticated():
    # Sidebar with user info and navigation
    with st.sidebar:
        st.write(f"� Welcome, **{auth.get_username()}**!")
        st.divider()
        
        st.write("**Available Chatbots:**")
        st.write("• 👨‍💼 Ian Cruz")
        st.write("• 🤖 Controller Agent")
        
        st.divider()
        
        if st.button("🚪 Logout"):
            auth.logout()
    
    # Main content area
    st.title("🚀 Chat Hub")
    st.write("Welcome to your personal chat hub! Choose a chatbot from the sidebar to get started.")
    
    # Chatbot cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👨‍💼 Chat with Ian Cruz")
        st.write("Personal assistant and knowledge expert ready to help with various topics and questions.")
        st.page_link("pages/1_Ian_Cruz.py", label="Start Chat with Ian", icon="💬")
    
    with col2:
        st.subheader("🤖 Controller Agent")
        st.write("System controller and automation assistant specialized in technical assistance and system management.")
        st.page_link("pages/2_Controller_Agent.py", label="Start Chat with Controller", icon="💬")
    
    st.divider()
    
    # System info (expandable)
    with st.expander("🔧 System Information"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**App Configuration:**")
            st.write(f"• App Name: {settings.APP_NAME}")
            st.write(f"• Version: {settings.APP_VERSION}")
            st.write(f"• Port: {settings.STREAMLIT_SERVER_PORT}")
        
        with col2:
            st.write("**Connected Services:**")
            st.write(f"• Database: {settings.POSTGRES_DB}")
            st.write(f"• LightRAG: {settings.LIGHTRAG_URL}")
            st.write(f"• Available Chatbots: {len(settings.CHATBOTS)}")
    
    # Footer
    st.markdown("---")
    st.markdown("*Built with Streamlit • Powered by LightRAG*")
