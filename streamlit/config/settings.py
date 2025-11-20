"""
Configuration settings for the Streamlit Chat App
"""
import os

class Settings:
    """Application settings loaded from environment variables"""
    
    # Database Configuration
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'n8n')
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'n8n')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'n8npassword')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', '5432'))
    
    # Streamlit Configuration
    STREAMLIT_SERVER_PORT = int(os.getenv('STREAMLIT_SERVER_PORT', '8501'))
    
    # App Configuration
    APP_NAME = "Chat Hub & Rental Market Analytics"
    APP_VERSION = "1.0.0"
    
    # Chatbot Configurations
    CHATBOTS = {
        "controller": {
            "name": "Financial Controller",
            "description": "Financial analysis and planning expert",
            "icon": "💰",
            "system_prompt": "You are a Financial Controller, specialized in financial planning, analysis, budgeting, and strategic financial decision-making."
        },
        "rental_dashboard": {
            "name": "Rental Market Dashboard",
            "description": "Real-time Zillow rental market analytics",
            "icon": "📊",
            "path": "pages/3_Rental_Market_Dashboard.py"
        }
    }

# Create a global settings instance
settings = Settings()
