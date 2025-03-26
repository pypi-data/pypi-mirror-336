#!/usr/bin/env python
"""
Example script demonstrating how to send a WhatsApp message using the WbizTool client.
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
    
    # Check if the API is operational
    print("Checking API status...")
    try:
        status = client.health_check()
        print(f"API Status: {status}")
    except Exception as e:
        print(f"Error checking API status: {e}")
        return
    
    # Set message parameters
    phone_number = "919876543210"  # Replace with the recipient's phone number
    message = "Hello from WbizTool Python Client! Sent at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Send a regular text message
    print(f"Sending text message to {phone_number}...")
    try:
        response = client.send_message(
            phone=phone_number,
            msg=message,
            country_code="91",  # Replace with the appropriate country code
            msg_type=0,  # 0 for text message
            webhook="https://your-webhook.com/callback",  # Optional webhook for delivery notifications
            expire_after_seconds=3600  # Optional: message expires after 1 hour if not delivered
        )
        print(f"Text message sent! Response: {response}")
        
        # If the message was sent successfully, we can get the message ID
        if response.get("status") == 1:
            msg_id = response.get("msg_id")
            print(f"Message ID: {msg_id}")
            
            # Check the message status
            print(f"Checking message status...")
            msg_status = client.get_message_status(msg_id)
            print(f"Message Status: {msg_status}")
            
            # Example of how to cancel a message
            print(f"Cancelling the message...")
            cancel_response = client.cancel_message(msg_id)
            print(f"Cancel response: {cancel_response}")
    except Exception as e:
        print(f"Error sending text message: {e}")
    
    # Example: Send a message with an image
    print(f"\nSending image message to {phone_number}...")
    try:
        image_response = client.send_message(
            phone=phone_number,
            msg="Check out this image!",
            country_code="91",
            msg_type=1,  # 1 for image message
            # Option 1: Use an image URL
            img_url="https://example.com/path/to/image.jpg"
            
            # Option 2: Upload a local image file
            # file_path="/path/to/local/image.jpg"
        )
        print(f"Image message sent! Response: {image_response}")
    except Exception as e:
        print(f"Error sending image message: {e}")
    
    # Example: Send a message with a document/file
    print(f"\nSending document message to {phone_number}...")
    try:
        document_response = client.send_message(
            phone=phone_number,
            msg="Here's the document you requested",
            country_code="91",
            msg_type=2,  # 2 for file/document message
            
            # Option 1: Use a file URL
            file_url="https://example.com/path/to/document.pdf",
            file_name="Important Document.pdf"
            
            # Option 2: Upload a local file
            # file_path="/path/to/local/document.pdf"
        )
        print(f"Document message sent! Response: {document_response}")
    except Exception as e:
        print(f"Error sending document message: {e}")
        
    # Get message history
    print("\nGetting message history...")
    try:
        report = client.get_messages_report(
            start_date="01-01-2023",  # DD-MM-YYYY format
            end_date="31-12-2023",    # DD-MM-YYYY format
            page=1
        )
        
        print(f"Found {report.get('total', 0)} messages in history")
        
        # Process the first few messages
        for msg in report.get('history', [])[:3]:
            print(f"Message ID: {msg.get('id')}, Status: {msg.get('message_status')}")
    except Exception as e:
        print(f"Error getting message history: {e}")

if __name__ == "__main__":
    main() 