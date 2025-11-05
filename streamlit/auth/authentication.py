"""
Basic authentication system for the Streamlit app
"""
import streamlit as st
import hashlib
import time

class Authentication:
    """Simple session-based authentication"""
    
    def __init__(self):
        # Initialize session state
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'username' not in st.session_state:
            st.session_state.username = None
    
    def hash_password(self, password: str) -> str:
        """Simple password hashing (use proper hashing in production)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login_form(self):
        """Display login form"""
        st.subheader("🔐 Login to Chat Hub")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                # Simple authentication (replace with database check)
                if self.authenticate_user(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    
    def register_form(self):
        """Display registration form"""
        st.subheader("📝 Register New Account")
        
        with st.form("register_form"):
            username = st.text_input("Choose Username")
            email = st.text_input("Email Address")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Register")
            
            if submitted:
                if password != confirm_password:
                    st.error("Passwords don't match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters")
                elif self.register_user(username, email, password):
                    st.success("Registration successful! You can now login.")
                else:
                    st.error("Username already exists")
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user (placeholder - replace with database check)"""
        # Temporary: Allow any user with password 'demo123'
        return password == 'demo123'
    
    def register_user(self, username: str, email: str, password: str) -> bool:
        """Register new user (placeholder - replace with database insert)"""
        # Placeholder implementation
        return True
    
    def logout(self):
        """Logout current user"""
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
    
    def get_username(self) -> str:
        """Get current username"""
        return st.session_state.get('username', '')
    
    def require_auth(self):
        """Decorator-like function to require authentication"""
        if not self.is_authenticated():
            st.title("🚀 Welcome to Chat Hub")
            st.write("Please login or register to access the chat features.")
            
            tab1, tab2 = st.tabs(["Login", "Register"])
            
            with tab1:
                self.login_form()
            
            with tab2:
                self.register_form()
            
            st.stop()

# Global auth instance
auth = Authentication()
