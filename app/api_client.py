"""API client for communicating with Langflow."""
import json
from typing import Dict, Optional, Union, Any
import requests
from .config import API_URL, HEADERS

class LangflowClient:
    """Client for interacting with the Langflow API."""
    
    def __init__(self, api_url: str = None, headers: Dict = None):
        """Initialize the Langflow client."""
        self.api_url = api_url or API_URL
        self.headers = headers or HEADERS
    
    def send_message(
        self, 
        message: str, 
        session_id: str,
        sender_name: str = "User",
        files: list = None
    ) -> str:
        """
        Send a message to the Langflow API and return the response.
        
        Args:
            message: The message text to send
            session_id: The session ID for conversation tracking
            sender_name: Name of the message sender
            files: List of files to include (not implemented)
            
        Returns:
            str: The API response text
        """
        if files is None:
            files = []
            
        payload = {
            "input_value": message,
            "output_type": "chat",
            "input_type": "chat",
            "tweaks": {
                "ChatInput-vEZZd": {
                    "files": files,
                    "sender_name": sender_name,
                    "session_id": session_id
                }
            }
        }
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            # Parse the JSON response
            response_data = response.json()
            
            # Extract the chat message from the nested structure
            try:
                # Navigate through the nested structure to find the message text
                if isinstance(response_data, dict):
                    outputs = response_data.get('outputs', [])
                    if outputs and isinstance(outputs, list) and len(outputs) > 0:
                        first_output = outputs[0]
                        if isinstance(first_output, dict):
                            outputs_list = first_output.get('outputs', [])
                            if outputs_list and isinstance(outputs_list, list) and len(outputs_list) > 0:
                                for output in outputs_list:
                                    if isinstance(output, dict) and 'results' in output:
                                        message_data = output['results'].get('message', {})
                                        if isinstance(message_data, dict) and 'data' in message_data:
                                            text = message_data['data'].get('text')
                                            if text:
                                                return text
            except (KeyError, AttributeError, TypeError) as e:
                # If any error occurs during parsing, fall through to the raw response
                pass
            
            # If we couldn't find the message in the expected format, return the raw response
            return str(response_data)
            
        except requests.exceptions.RequestException as e:
            return f"Error connecting to Langflow API: {str(e)}"
        except json.JSONDecodeError:
            return response.text.strip('\"')
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
