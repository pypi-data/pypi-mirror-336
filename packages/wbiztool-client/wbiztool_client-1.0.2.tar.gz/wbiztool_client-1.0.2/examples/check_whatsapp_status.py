#!/usr/bin/env python
"""
Example script demonstrating how to check WhatsApp client status
using the WbizTool client.
"""

import os
import sys

# Add the parent directory to the path so we can import the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wbiztool_client import WbizToolClient

def main():
    # Replace with your own API key and client ID
    API_KEY = "your_api_key"
    CLIENT_ID = "your_client_id"  # Optional
    
    # Initialize the client
    client = WbizToolClient(api_key=API_KEY, client_id=CLIENT_ID)
    
    # Check status of all WhatsApp clients
    print("Checking status of all WhatsApp clients...")
    try:
        all_status = client.get_whatsapp_client_status()
        print(f"All clients status: {all_status}")
        
        # Print a more readable version if available
        if "whatsapp_clients" in all_status:
            for wa_client in all_status["whatsapp_clients"]:
                print(f"Client ID: {wa_client.get('id')}")
                print(f"  Name: {wa_client.get('name')}")
                print(f"  Status: {wa_client.get('status')}")
                print(f"  Connected: {wa_client.get('is_connected', False)}")
                print("")
    except Exception as e:
        print(f"Error checking all clients: {e}")
    
    # Check status of a specific WhatsApp client
    # Replace with an actual client ID from your account
    WHATSAPP_CLIENT_ID = 123  # Replace with your actual WhatsApp client ID
    
    print(f"\nChecking status of specific WhatsApp client (ID: {WHATSAPP_CLIENT_ID})...")
    try:
        specific_status = client.get_specific_whatsapp_client_status(WHATSAPP_CLIENT_ID)
        print(f"Specific client status: {specific_status}")
        
        # Alternative method to check specific client
        print("\nUsing the alternative method:")
        alt_status = client.get_whatsapp_client_status(whatsapp_client_id=WHATSAPP_CLIENT_ID)
        print(f"Status: {alt_status}")
    except Exception as e:
        print(f"Error checking specific client: {e}")
    
    # List all WhatsApp clients (to find available client IDs)
    print("\nListing all WhatsApp clients...")
    try:
        clients = client.list_whatsapp_clients()
        print(f"Available clients: {clients}")
    except Exception as e:
        print(f"Error listing clients: {e}")

if __name__ == "__main__":
    main() 