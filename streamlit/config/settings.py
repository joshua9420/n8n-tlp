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
    
    # LightRAG Configuration
    LIGHTRAG_URL = os.getenv('LIGHTRAG_URL', 'http://lightrag:9621')
    LIGHTRAG_API_KEY = os.getenv('LIGHTRAG_API_KEY', 'changeme')
    
    # Streamlit Configuration
    STREAMLIT_SERVER_PORT = int(os.getenv('STREAMLIT_SERVER_PORT', '8501'))
    
    # App Configuration
    APP_NAME = "Chat Hub"
    APP_VERSION = "1.0.0"
    
    # Chatbot Configurations
    CHATBOTS = {
        "ian_cruz": {
            "name": "Chat with Ian Cruz",
            "description": "Personal assistant and knowledge expert",
            "icon": "👨‍💼",
            "system_prompt": "You are Ian Cruz, a knowledgeable assistant ready to help with various topics and questions."
        },
        "controller": {
            "name": "Financial Controller",
            "description": "Financial analysis and planning expert",
            "icon": "💰",
            "system_prompt": "You are a Financial Controller, specialized in financial planning, analysis, budgeting, and strategic financial decision-making."
        }
    }

# Create a global settings instance
settings = Settings()
