"""
Ian Cruz Chatbot Page
"""
import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import auth
from chat import IanCruzChat

# Page configuration
st.set_page_config(
    page_title="Chat with Ian Cruz",
    page_icon="👨‍💼",
    layout="wide"
)

# Require authentication
auth.require_auth()

# Main content
if auth.is_authenticated():
    # Clean, compact sidebar
    with st.sidebar:
        st.write(f"👋 **{auth.get_username()}**")
        st.divider()
        
        # Current chatbot info
        st.markdown("**👨‍💼 Ian Cruz**")
        st.caption("Personal assistant and knowledge expert")
        
        # Message count
        if f"messages_ian_cruz" in st.session_state:
            msg_count = len(st.session_state[f"messages_ian_cruz"])
            st.metric("💬 Messages", msg_count, delta=None)
        
        st.divider()
        
        # Compact navigation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Hub", use_container_width=True):
                st.switch_page("app.py")
        with col2:
            if st.button("💰 Finance", use_container_width=True):
                st.switch_page("pages/2_Controller_Agent.py")
        
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            auth.logout()
    
    # Chat interface
    ian_chat = IanCruzChat()
    ian_chat.display_chat_interface()
