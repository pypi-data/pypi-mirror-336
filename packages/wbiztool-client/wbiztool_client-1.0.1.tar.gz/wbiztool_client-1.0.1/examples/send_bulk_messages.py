#!/usr/bin/env python
"""
Example script demonstrating how to send WhatsApp messages to multiple recipients
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
    phone_numbers = [
        "919876543210",  # Replace with real phone numbers
        "919876543211",
        "919876543212"
    ]
    
    message = "Hello everyone! This is a bulk message sent at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Send a text message to multiple recipients
    print(f"Sending bulk text message to {len(phone_numbers)} recipients...")
    try:
        response = client.send_bulk_messages(
            phones=phone_numbers,
            msg=message,
            country_code="91",  # Replace with the appropriate country code
            msg_type=0  # 0 for text message
        )
        print(f"Bulk text message sent! Response: {response}")
        
        # If successful, you might get multiple message IDs back
        if response.get("status") == 1:
            msg_ids = response.get("msg_ids", [])
            print(f"Message IDs: {msg_ids}")
    except Exception as e:
        print(f"Error sending bulk text message: {e}")
    
    # Example: Send a document to multiple recipients
    print(f"\nSending document to {len(phone_numbers)} recipients...")
    try:
        document_response = client.send_bulk_messages(
            phones=phone_numbers,
            msg="Here's the document everyone requested",
            country_code="91",
            msg_type=2,  # 2 for file/document message
            file_url="https://example.com/path/to/document.pdf",
            file_name="Group Document.pdf"
        )
        print(f"Bulk document message sent! Response: {document_response}")
    except Exception as e:
        print(f"Error sending bulk document message: {e}")
    
    # Example: Sending a message with a locally uploaded file to multiple recipients
    print(f"\nSending a local file to {len(phone_numbers)} recipients...")
    try:
        # Create a temporary test file (in a real scenario, you'd use an existing file)
        test_file_path = "temp_test_file.txt"
        with open(test_file_path, "w") as f:
            f.write("This is a test file created for the bulk message example")
        
        # Send the file to multiple recipients
        local_file_response = client.send_bulk_messages(
            phones=phone_numbers,
            msg="Here's a file uploaded directly from our system",
            country_code="91",
            msg_type=2,  # 2 for file/document
            file_path=test_file_path
        )
        print(f"Local file bulk message sent! Response: {local_file_response}")
        
        # Clean up the temporary file
        os.remove(test_file_path)
    except Exception as e:
        print(f"Error sending local file in bulk: {e}")
        # Clean up in case of error
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

if __name__ == "__main__":
    main() 