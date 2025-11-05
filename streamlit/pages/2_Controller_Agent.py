"""
Controller Agent Chatbot Page
"""
import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import auth
from chat import ControllerAgentChat

# Page configuration
st.set_page_config(
    page_title="Controller Agent",
    page_icon="🤖",
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
        st.markdown("**💰 Financial Controller**")
        st.caption("Financial analysis and planning expert")
        
        # Message count
        if f"messages_controller" in st.session_state:
            msg_count = len(st.session_state[f"messages_controller"])
            st.metric("💬 Messages", msg_count, delta=None)
        
        st.divider()
        
        # Compact navigation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Hub", use_container_width=True):
                st.switch_page("app.py")
        with col2:
            if st.button("👨‍💼 Ian", use_container_width=True):
                st.switch_page("pages/1_Ian_Cruz.py")
        
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            auth.logout()
    
    # Chat interface
    try:
        controller_chat = ControllerAgentChat()
        controller_chat.display_chat_interface()
    except Exception as e:
        st.error(f"Error initializing Financial Controller: {str(e)}")
        st.info("Please check your configuration and try again.")
