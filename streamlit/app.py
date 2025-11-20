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
        st.write(f"👋 **{auth.get_username()}**")
        st.divider()
        
        st.write("**Available Features:**")
        st.write("• 💰 Financial Controller")
        st.write("• 📊 Rental Market Dashboard")
        
        st.divider()
        
        if st.button("🚪 Logout"):
            auth.logout()
    
    # Main content area
    st.title("🚀 Chat Hub")
    st.write("Welcome to your Financial Controller chat assistant and Rental Market Dashboard.")
    
    # Application cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Financial Controller")
        st.write("Financial analysis and planning expert specialized in budgeting, cash flow management, and strategic financial decision-making.")
        st.page_link("pages/2_Controller_Agent.py", label="Start Chat with Financial Controller", icon="💬", use_container_width=True)
    
    with col2:
        st.subheader("📊 Rental Market Dashboard")
        st.write("Real-time analytics and insights from Zillow rental data. Track market trends, compare ZIP codes, and analyze property listings.")
        st.page_link("pages/3_Rental_Market_Dashboard.py", label="Open Rental Market Dashboard", icon="📈", use_container_width=True)
    
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
            st.write(f"• n8n Webhook: Configured")
            st.write(f"• Available Features: 2")
    
    # Footer
    st.markdown("---")
    st.markdown("*Built with Streamlit • Powered by n8n*")
