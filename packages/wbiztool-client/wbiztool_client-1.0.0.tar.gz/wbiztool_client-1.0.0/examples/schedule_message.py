#!/usr/bin/env python
"""
Example script demonstrating how to schedule WhatsApp messages using the WbizTool client.
"""

import os
import sys
from datetime import datetime, timedelta

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
    phone_number = "919876543210"  # Replace with the recipient's phone number
    
    # Schedule a message for 5 minutes from now
    schedule_time_1 = (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
    message_1 = f"This is scheduled message #1, set to be delivered at: {schedule_time_1}"
    
    # Schedule another message for 10 minutes from now
    schedule_time_2 = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
    message_2 = f"This is scheduled message #2, set to be delivered at: {schedule_time_2}"
    
    # Send the first scheduled message
    print(f"Scheduling message #1 for {schedule_time_1}...")
    try:
        response_1 = client.schedule_message(
            phone=phone_number,
            msg=message_1,
            schedule_time=schedule_time_1,
            country_code="91"  # Replace with the appropriate country code
        )
        print(f"Message #1 scheduled! Response: {response_1}")
        
        # Get the message ID
        if response_1.get("status") == 1:
            msg_id_1 = response_1.get("msg_id")
            print(f"Message #1 ID: {msg_id_1}")
    except Exception as e:
        print(f"Error scheduling message #1: {e}")
        return
    
    # Send the second scheduled message
    print(f"Scheduling message #2 for {schedule_time_2}...")
    try:
        response_2 = client.schedule_message(
            phone=phone_number,
            msg=message_2,
            schedule_time=schedule_time_2,
            country_code="91"  # Replace with the appropriate country code
        )
        print(f"Message #2 scheduled! Response: {response_2}")
        
        # Get the message ID
        if response_2.get("status") == 1:
            msg_id_2 = response_2.get("msg_id")
            print(f"Message #2 ID: {msg_id_2}")
            
            # Cancel the second message to demonstrate cancellation
            print(f"Cancelling message #2...")
            cancel_response = client.cancel_message(msg_id_2)
            print(f"Message #2 cancelled! Response: {cancel_response}")
    except Exception as e:
        print(f"Error with message #2: {e}")
    
    print("\nScript completed. Message #1 should be delivered at the scheduled time.")
    print("Message #2 was scheduled but then cancelled for demonstration purposes.")

if __name__ == "__main__":
    main() 