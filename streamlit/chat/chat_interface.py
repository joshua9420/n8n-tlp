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
            
            print(f"\n{'='*80}")
            print(f"[CONTROLLER CHAT] Starting request to n8n webhook")
            print(f"[CONTROLLER CHAT] URL: {url}")
            print(f"[CONTROLLER CHAT] User Query: {query[:100]}...")
            
            # Basic authentication
            username = "admin"
            password = "tlp123"
            auth_string = f"{username}:{password}"
            auth_bytes = auth_string.encode('utf-8')
            auth_b64 = base64.b64encode(auth_bytes).decode('utf-8')
            
            print(f"[CONTROLLER CHAT] Auth configured: Basic {auth_b64[:20]}...")
            
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
            
            print(f"[CONTROLLER CHAT] Payload prepared:")
            print(f"  - Message length: {len(query)} chars")
            print(f"  - Conversation history: {len(context_messages)} messages")
            print(f"  - Chatbot type: financial_controller")
            
            # Make the POST request to n8n webhook
            print(f"[CONTROLLER CHAT] Sending POST request...")
            response = requests.post(url, headers=headers, json=payload, timeout=45)
            
            print(f"[CONTROLLER CHAT] Response received:")
            print(f"  - Status Code: {response.status_code}")
            print(f"  - Response Headers: {dict(response.headers)}")
            print(f"  - Content-Type: {response.headers.get('Content-Type', 'Not specified')}")
            print(f"  - Response Length: {len(response.text)} chars")
            print(f"  - Response Text (first 1000 chars): {response.text[:1000]}")
            
            if response.status_code == 200:
                # Check if response is empty
                if not response.text or response.text.strip() == '':
                    print(f"[CONTROLLER CHAT] ERROR: Empty response body")
                    print(f"{'='*80}\n")
                    return "❌ n8n webhook returned empty response. Please check your workflow configuration."
                
                # Check content type
                content_type = response.headers.get('Content-Type', '')
                
                # Try to parse JSON first
                try:
                    result = response.json()
                    print(f"[CONTROLLER CHAT] Successfully parsed JSON response")
                except json.JSONDecodeError as je:
                    print(f"[CONTROLLER CHAT] Response is not JSON, treating as plain text")
                    print(f"  - JSON Error: {str(je)}")
                    print(f"  - Content-Type: {content_type}")
                    print(f"  - Returning plain text response")
                    print(f"{'='*80}\n")
                    # Return the plain text response directly
                    return response.text.strip()
                
                print(f"[CONTROLLER CHAT] Parsing JSON response:")
                print(f"  - Successfully parsed JSON")
                print(f"  - Type: {type(result)}")
                print(f"  - Is List: {isinstance(result, list)}")
                if isinstance(result, list):
                    print(f"  - List Length: {len(result)}")
                    if len(result) > 0:
                        print(f"  - First Item Type: {type(result[0])}")
                        print(f"  - First Item: {result[0]}")
                
                # Handle n8n webhook response format
                # n8n can return an array of objects or a single object
                if isinstance(result, list) and len(result) > 0:
                    print(f"[CONTROLLER CHAT] Processing array response...")
                    # If it's an array, get the first item
                    first_item = result[0]
                    if isinstance(first_item, dict):
                        # Try different possible response fields
                        extracted_response = (first_item.get('output') or 
                               first_item.get('response') or 
                               first_item.get('answer') or 
                               first_item.get('message') or 
                               first_item.get('result') or
                               'No response received from n8n workflow')
                        print(f"[CONTROLLER CHAT] Extracted response (first 200 chars): {str(extracted_response)[:200]}")
                        print(f"{'='*80}\n")
                        return extracted_response
                    else:
                        print(f"[CONTROLLER CHAT] First item is not a dict, converting to string")
                        print(f"{'='*80}\n")
                        return str(first_item)
                elif isinstance(result, dict):
                    print(f"[CONTROLLER CHAT] Processing dict response...")
                    # If it's a single object, try different possible response fields
                    extracted_response = (result.get('output') or
                           result.get('response') or 
                           result.get('answer') or 
                           result.get('message') or 
                           result.get('result') or
                           'No response received from n8n workflow')
                    print(f"[CONTROLLER CHAT] Extracted response (first 200 chars): {str(extracted_response)[:200]}")
                    print(f"{'='*80}\n")
                    return extracted_response
                else:
                    print(f"[CONTROLLER CHAT] Unknown response format, converting to string")
                    print(f"{'='*80}\n")
                    return str(result)
            elif response.status_code == 401:
                print(f"[CONTROLLER CHAT] ERROR: Authentication failed (401)")
                print(f"{'='*80}\n")
                return "🔐 Authentication failed with n8n webhook."
            elif response.status_code == 404:
                print(f"[CONTROLLER CHAT] ERROR: Webhook not found (404)")
                print(f"{'='*80}\n")
                return "🔍 n8n webhook not found. Please check the webhook URL configuration."
            elif response.status_code == 500:
                print(f"[CONTROLLER CHAT] ERROR: Server error (500)")
                print(f"  - Response: {response.text[:200]}")
                print(f"{'='*80}\n")
                return "⚠️ n8n workflow is experiencing issues. Please try again later."
            else:
                print(f"[CONTROLLER CHAT] ERROR: Unexpected status code {response.status_code}")
                print(f"  - Response: {response.text[:200]}")
                print(f"{'='*80}\n")
                return f"❌ n8n Webhook Error: Status {response.status_code} - {response.text[:200]}"
                
        except json.JSONDecodeError as e:
            print(f"[CONTROLLER CHAT] ERROR: JSON decode error (in exception handler)")
            print(f"  - Error: {str(e)}")
            print(f"  - Response text: {response.text[:1000] if 'response' in locals() else 'N/A'}")
            print(f"  - Response status: {response.status_code if 'response' in locals() else 'N/A'}")
            print(f"{'='*80}\n")
            return f"� Invalid JSON from n8n. Response: {response.text[:200] if 'response' in locals() else 'N/A'}"
        except requests.exceptions.ConnectionError as e:
            print(f"[CONTROLLER CHAT] ERROR: Connection error")
            print(f"  - Error: {str(e)}")
            print(f"{'='*80}\n")
            return "🔌 Cannot connect to n8n webhook. Please check if n8n is running and accessible."
        except requests.exceptions.Timeout as e:
            print(f"[CONTROLLER CHAT] ERROR: Request timeout")
            print(f"  - Error: {str(e)}")
            print(f"{'='*80}\n")
            return "⏱️ Request timed out. The n8n workflow might be processing a complex request."
        except requests.exceptions.RequestException as e:
            print(f"[CONTROLLER CHAT] ERROR: Request exception")
            print(f"  - Error: {str(e)}")
            print(f"{'='*80}\n")
            return f"🌐 Network error connecting to n8n: {str(e)}"
        except Exception as e:
            print(f"[CONTROLLER CHAT] ERROR: Unexpected exception")
            print(f"  - Type: {type(e).__name__}")
            print(f"  - Error: {str(e)}")
            import traceback
            print(f"  - Traceback:\n{traceback.format_exc()}")
            print(f"{'='*80}\n")
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
