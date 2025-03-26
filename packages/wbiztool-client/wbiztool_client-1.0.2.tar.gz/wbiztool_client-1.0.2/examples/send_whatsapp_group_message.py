#!/usr/bin/env python
"""
Example script demonstrating how to send WhatsApp messages to a WhatsApp group
using the WbizTool client.
"""

import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wbiztool_client import WbizToolClient

def main():
    # Replace with your own API key and client ID
    API_KEY = "your_api_key"
    CLIENT_ID = "your_client_id"  # Optional
    
    # Initialize the client
    client = WbizToolClient(api_key=API_KEY, client_id=CLIENT_ID)
    
    # Set message parameters
    group_name = "Family Group"  # Replace with the exact name of your WhatsApp group
    message = "Hello group! This is a message sent at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Send a text message to the WhatsApp group
    print(f"Sending text message to WhatsApp group '{group_name}'...")
    try:
        response = client.send_message_to_group(
            group_name=group_name,
            msg=message,
            msg_type=0  # 0 for text message
        )
        print(f"Group message sent! Response: {response}")
        
        # If the message was sent successfully, we can get the message ID
        if response.get("status") == 1:
            msg_id = response.get("msg_id")
            print(f"Message ID: {msg_id}")
    except Exception as e:
        print(f"Error sending message to group: {e}")
    
    # Example: Send an image to the WhatsApp group
    print(f"\nSending image to WhatsApp group '{group_name}'...")
    try:
        image_response = client.send_message_to_group(
            group_name=group_name,
            msg="Check out this image!",
            msg_type=1,  # 1 for image message
            # Option 1: Use an image URL
            img_url="https://example.com/path/to/image.jpg"
            
            # Option 2: Upload a local image file
            # file_path="/path/to/local/image.jpg"
        )
        print(f"Image message sent to group! Response: {image_response}")
    except Exception as e:
        print(f"Error sending image message to group: {e}")
    
    # Example: Send a document/file to the WhatsApp group
    print(f"\nSending document to WhatsApp group '{group_name}'...")
    try:
        document_response = client.send_message_to_group(
            group_name=group_name,
            msg="Here's the document for everyone",
            msg_type=2,  # 2 for file/document message
            
            # Option 1: Use a file URL
            file_url="https://example.com/path/to/document.pdf",
            file_name="Group Document.pdf"
            
            # Option 2: Upload a local file
            # file_path="/path/to/local/document.pdf"
        )
        print(f"Document sent to group! Response: {document_response}")
    except Exception as e:
        print(f"Error sending document to group: {e}")

if __name__ == "__main__":
    main() 