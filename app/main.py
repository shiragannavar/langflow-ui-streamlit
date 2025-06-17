"""
Langflow Chat UI

A Streamlit-based interface for interacting with Langflow's API.
"""
import streamlit as st
from .api_client import LangflowClient
from .config import DEFAULT_SESSION_ID, MAX_CHAT_HISTORY

# Initialize the Langflow client
client = LangflowClient()

# Page configuration
st.set_page_config(
    page_title="Langflow Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize the session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = DEFAULT_SESSION_ID
    if "session_initialized" not in st.session_state:
        st.session_state.session_initialized = False

def display_chat_messages():
    """Display chat messages from the session state."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input():
    """Handle user input and get response from Langflow API."""
    if prompt := st.chat_input("Type your message..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.send_message(
                    message=prompt,
                    session_id=st.session_state.session_id
                )
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Limit chat history size
        if len(st.session_state.messages) > MAX_CHAT_HISTORY * 2:  # *2 for user/assistant pairs
            st.session_state.messages = st.session_state.messages[-MAX_CHAT_HISTORY * 2:]

def show_session_sidebar():
    """Display the session management sidebar."""
    with st.sidebar:
        st.title("Session Settings")
        
        # Session ID input
        new_session_id = st.text_input(
            "Session ID",
            value=st.session_state.session_id,
            key="session_input"
        )
        
        # Update session ID if changed
        if new_session_id != st.session_state.session_id:
            st.session_state.session_id = new_session_id
            st.session_state.messages = []
            st.rerun()
        
        # Clear chat button
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        # Display session info
        st.divider()
        st.caption(f"Current Session: `{st.session_state.session_id}`")
        st.caption(f"Messages in history: {len(st.session_state.messages) // 2}")

def main():
    """Main application function."""
    initialize_session_state()
    
    # Page header
    st.title("💬 Langflow Chat")
    
    # Show session sidebar
    show_session_sidebar()
    
    # Display chat messages
    display_chat_messages()
    
    # Handle user input
    handle_user_input()

if __name__ == "__main__":
    main()
