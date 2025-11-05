"""
Chat interface components for different chatbots
"""
import streamlit as st
import requests
import json
import time
import base64
from datetime import datetime
from config import settings

class ChatInterface:
    """Base chat interface for chatbots"""
    
    def __init__(self, chatbot_key: str):
        self.chatbot_key = chatbot_key
        self.chatbot_config = settings.CHATBOTS[chatbot_key]
        
        # Initialize session state for this chatbot
        self.messages_key = f"messages_{chatbot_key}"
        if self.messages_key not in st.session_state:
            st.session_state[self.messages_key] = []
    
    def display_header(self):
        """Display compact chatbot header"""
        # Compact header with icon and name in one line
        st.markdown(f"### {self.chatbot_config['icon']} {self.chatbot_config['name']}")
        st.caption(self.chatbot_config['description'])
    
    def display_chat_history(self):
        """Display chat messages"""
        for message in st.session_state[self.messages_key]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "timestamp" in message:
                    st.caption(f"📅 {message['timestamp']}")
    
    def add_message(self, role: str, content: str):
        """Add message to chat history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state[self.messages_key].append({
            "role": role,
            "content": content,
            "timestamp": timestamp
        })
    
    def clear_chat(self):
        """Clear chat history"""
        st.session_state[self.messages_key] = []
        st.rerun()
    
    def get_lightrag_response(self, query: str) -> str:
        """Get response from LightRAG API"""
        try:
            url = f"{settings.LIGHTRAG_URL}/query"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.LIGHTRAG_API_KEY}"
            }
            
            # Customize the query based on chatbot type
            system_prompt = self.chatbot_config['system_prompt']
            enhanced_query = f"{system_prompt}\n\nUser Query: {query}"
            
            payload = {
                "query": enhanced_query,
                "mode": "hybrid"  # or "local", "global" depending on your needs
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response received from LightRAG')
            else:
                return f"Error: LightRAG API returned status {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return f"Error connecting to LightRAG: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def display_chat_interface(self):
        """Main chat interface"""
        self.display_header()
        
        # Chat controls
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("🗑️ Clear Chat", help="Clear all messages"):
                self.clear_chat()
        
        # Display chat history
        self.display_chat_history()
        
        # Chat input
        if prompt := st.chat_input(f"Message {self.chatbot_config['name']}..."):
            # Add user message
            self.add_message("user", prompt)
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = self.get_lightrag_response(prompt)
                st.markdown(response)
                self.add_message("assistant", response)

class IanCruzChat(ChatInterface):
    """Specialized chat interface for Ian Cruz"""
    
    def __init__(self):
        super().__init__("ian_cruz")
    
    def display_header(self):
        """Compact header for Ian Cruz"""
        super().display_header()
        st.success("💡 **Ask me about**: Business Insights • Productivity Tips • General Knowledge", icon="👨‍💼")

class ControllerAgentChat(ChatInterface):
    """Specialized chat interface for Financial Controller"""
    
    def __init__(self):
        super().__init__("controller")
    
    def display_header(self):
        """Compact header for Financial Controller"""
        super().display_header()
        # More compact tip using success instead of info
        st.success("� **Ask me about**: Budgets • Financial Analysis • Cash Flow • Investments • Financial Planning", icon="💰")
    
    def get_controller_response(self, query: str, conversation_history: list = None) -> str:
        """Get response from Financial Controller via n8n webhook"""
        try:
            url = "https://n8n.srv1075445.hstgr.cloud/webhook/financial-controller-chatbot"
            
            # Basic authentication
            username = "admin"
            password = "tlp123"
            auth_string = f"{username}:{password}"
            auth_bytes = auth_string.encode('utf-8')
            auth_b64 = base64.b64encode(auth_bytes).decode('utf-8')
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Basic {auth_b64}"
            }
            
            # Enhanced system prompt for Financial Controller Agent
            system_prompt = """You are a Financial Controller Agent, an advanced AI assistant specialized in:
            - Financial planning, analysis, and reporting
            - Budget management and variance analysis
            - Cash flow forecasting and management
            - Financial compliance and regulatory requirements
            - Cost control and expense management
            - Financial risk assessment and mitigation
            - Investment analysis and capital allocation
            - Management accounting and performance metrics
            - Financial audit preparation and support
            - Strategic financial decision-making
            
            Provide detailed, actionable financial insights with step-by-step analysis when appropriate.
            Always consider financial accuracy, compliance requirements, and best practices in your recommendations.
            Support your analysis with relevant financial ratios, metrics, and industry benchmarks where applicable."""
            
            # Build conversation context - maintain dictionary format
            context_messages = []
            context_str_list = []
            if conversation_history:
                # Include recent conversation history for context
                for msg in conversation_history[-5:]:  # Last 5 messages for context
                    # Keep original dictionary format for API
                    context_messages.append({
                        "role": msg['role'],
                        "content": msg['content'],
                        "timestamp": msg.get('timestamp', '')
                    })
                    # Create string version for full_prompt
                    context_str_list.append(f"{msg['role'].title()}: {msg['content']}")
            
            # Construct the full prompt using string format
            context_str = "\n".join(context_str_list) if context_str_list else ""
            full_prompt = f"{system_prompt}\n\nConversation History:\n{context_str}\n\nCurrent Query: {query}"
            
            # Payload for n8n webhook
            payload = {
                "message": query,
                "system_prompt": system_prompt,
                "conversation_history": context_messages,  # List of dictionaries
                "full_prompt": full_prompt,
                "chatbot_type": "financial_controller",
                "timestamp": datetime.now().isoformat()
            }
            
            # Make the POST request to n8n webhook
            response = requests.post(url, headers=headers, json=payload, timeout=45)
            
            if response.status_code == 200:
                result = response.json()
                # Handle n8n webhook response format
                if isinstance(result, dict):
                    # Try different possible response fields from n8n
                    return (result.get('response') or 
                           result.get('answer') or 
                           result.get('message') or 
                           result.get('output') or 
                           result.get('result') or
                           'No response received from n8n workflow')
                else:
                    return str(result)
            elif response.status_code == 401:
                return "🔐 Authentication failed with n8n webhook."
            elif response.status_code == 404:
                return "🔍 n8n webhook not found. Please check the webhook URL configuration."
            elif response.status_code == 500:
                return "⚠️ n8n workflow is experiencing issues. Please try again later."
            else:
                return f"❌ n8n Webhook Error: Status {response.status_code} - {response.text[:200]}"
                
        except requests.exceptions.ConnectionError:
            return "🔌 Cannot connect to n8n webhook. Please check if n8n is running and accessible."
        except requests.exceptions.Timeout:
            return "⏱️ Request timed out. The n8n workflow might be processing a complex request."
        except requests.exceptions.RequestException as e:
            return f"🌐 Network error connecting to n8n: {str(e)}"
        except json.JSONDecodeError:
            return "📄 Invalid response format from n8n workflow."
        except Exception as e:
            return f"💥 Unexpected error: {str(e)}"
    
    def display_chat_interface(self):
        """Compact chat interface for Financial Controller"""
        # Compact header and controls in same row
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"### {self.chatbot_config['icon']} {self.chatbot_config['name']}")
            st.caption(self.chatbot_config['description'])
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Small spacing
            if st.button("🗑️ Clear", help="Clear all messages", use_container_width=True):
                self.clear_chat()
        
        # Compact tip
        st.success("💡 **Ask me about**: Budgets • Analysis • Cash Flow • Investments • Planning", icon="💰")
        
        # Chat messages
        for message in st.session_state[self.messages_key]:
            with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
                st.markdown(message["content"])
        
        # Main chat input
        if prompt := st.chat_input("Ask the Controller Agent anything...", key="controller_input"):
            self._process_user_message(prompt)
    
    def _process_user_message(self, prompt: str):
        """Process user message and get AI response"""
        # Add user message
        self.add_message("user", prompt)
        
        # Display user message immediately
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Get and display assistant response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤖 Controller Agent is analyzing..."):
                # Get conversation history for context
                conversation_history = st.session_state[self.messages_key]
                response = self.get_controller_response(prompt, conversation_history)
            
            # Display response
            st.markdown(response)
        
        # Add assistant response to history
        self.add_message("assistant", response)
