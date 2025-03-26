"""WbizTool API client for Python."""

import json
import requests
from typing import Dict, List, Union, Optional, Any, BinaryIO
import os


class WbizToolClient:
    """Client for the WbizTool API."""

    BASE_URL = "https://wbiztool.com/api/v1"

    def __init__(self, api_key: Optional[str] = None, client_id: Optional[int] = None, validate_credentials: bool = False):
        """
        Initialize a new WbizTool API client.

        Args:
            api_key: Your WbizTool API key. If not provided, will try to read from WBIZTOOL_API_KEY environment variable.
            client_id: Your WbizTool client ID. If not provided, will try to read from WBIZTOOL_CLIENT_ID environment variable.
            validate_credentials: If True, will validate the credentials immediately by making an API call.
        
        Raises:
            ValueError: If API key is not provided as a parameter or found in environment variables.
            requests.exceptions.HTTPError: If validate_credentials is True and the credentials are invalid.
        """
        # Try to get API key from parameter or environment variable
        self.api_key = api_key or os.environ.get("WBIZTOOL_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either as a parameter or set in WBIZTOOL_API_KEY environment variable")
            
        # Try to get client ID from parameter or environment variable
        client_id_str = os.environ.get("WBIZTOOL_CLIENT_ID")
        if client_id is not None:
            self.client_id = client_id
        elif client_id_str:
            try:
                self.client_id = int(client_id_str)
            except ValueError:
                raise ValueError(f"Invalid client ID in environment variable: {client_id_str}. Must be an integer.")
        else:
            self.client_id = None
            
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
        })
        
        # Validate credentials if requested
        if validate_credentials:
            self.check_credentials()

    def _make_request(self, method: str, endpoint: str, data: Dict = None, files: Dict = None) -> Dict:
        """
        Make a request to the WbizTool API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            data: Request data
            files: Files to upload

        Returns:
            API response as a dictionary
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        # Always include API key and client_id in the data
        if data is None:
            data = {}
        
        if 'api_key' not in data:
            data['api_key'] = self.api_key
        if 'client_id' not in data and self.client_id:
            data['client_id'] = self.client_id
            
        if method.upper() == 'GET':
            response = self.session.get(url, params=data)
        else:
            if files:
                # For multipart form data (file uploads)
                response = self.session.request(method, url, data=data, files=files)
            else:
                # For normal JSON data
                response = self.session.request(method, url, data=data)
        
        response.raise_for_status()
        
        if response.content:
            return response.json()
        return {}

    def health_check(self) -> Dict:
        """
        Check if the API is operational.
        
        Returns:
            API status information
        """
        return self._make_request("GET", "/status/")
    
    def check_credentials(self) -> Dict:
        """
        Verify the API credentials.
        
        Returns:
            Credentials validation result
            
        Raises:
            ValueError: If the credentials are invalid or there's an authentication error
        """
        try:
            response = self._make_request("GET", "/me/")
            
            # Check if the API returned an error status
            if response.get('status') == 0:
                error_msg = response.get('message', 'Authentication failed')
                raise ValueError(f"Invalid credentials: {error_msg}")
                
            return response
            
        except requests.exceptions.HTTPError as e:
            # Handle HTTP errors (like 400 status code)
            if e.response.status_code == 400:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('message', 'Authentication failed')
                    raise ValueError(f"Invalid credentials: {error_msg}") from e
                except (ValueError, json.JSONDecodeError):
                    # If we can't parse the error response
                    raise ValueError("Invalid credentials") from e
            else:
                # Re-raise other HTTP errors
                raise

    def send_message(self, phone: str, msg: str, country_code: str = None, 
                    whatsapp_client: Union[int, str] = None, msg_type: Union[int, str] = 0,
                    file_url: str = None, file_name: str = None, img_url: str = None,
                    file_path: str = None, webhook: str = None, 
                    expire_after_seconds: int = None) -> Dict:
        """
        Send a WhatsApp message.
        
        Args:
            phone: Recipient's phone number
            msg: Message content
            country_code: Country code (e.g., "91" for India)
            whatsapp_client: Specific WhatsApp client ID to use
            msg_type: Message type (0=text, 1=image, 2=file)
            file_url: URL of a file to send (use for msg_type=2)
            file_name: Name for the file (required for msg_type=2)
            img_url: URL of an image to send (use for msg_type=1)
            file_path: Path to a local file to upload (alternative to file_url/img_url)
            webhook: Webhook URL for delivery notifications
            expire_after_seconds: Time after which the message expires if not delivered
            
        Returns:
            Message sending result with message ID
        """
        data = {
            "phone": phone,
            "msg": msg,
            "msg_type": msg_type
        }
        
        # Add optional parameters if provided
        if country_code:
            data["country_code"] = country_code
        if whatsapp_client:
            data["whatsapp_client"] = whatsapp_client
        if webhook:
            data["webhook"] = webhook
        if expire_after_seconds:
            data["expire_after_seconds"] = expire_after_seconds
            
        files = None
        
        # Handle message type and related parameters
        msg_type = str(msg_type)
        if msg_type == "1":  # Image message
            if img_url:
                data["img_url"] = img_url
            elif file_path and os.path.exists(file_path):
                files = {'file': open(file_path, 'rb')}
            else:
                raise ValueError("For image messages (msg_type=1), either img_url or file_path must be provided")
                
        elif msg_type == "2":  # File message
            if file_name:
                data["file_name"] = file_name
            elif file_path:
                # Extract filename from path if not provided
                data["file_name"] = os.path.basename(file_path)
                
            if file_url:
                data["file_url"] = file_url
            elif file_path and os.path.exists(file_path):
                files = {'file': open(file_path, 'rb')}
            else:
                raise ValueError("For file messages (msg_type=2), either file_url or file_path must be provided")
            
        return self._make_request("POST", "/send_msg/", data, files)
    
    def send_message_to_group(self, group_name: str, msg: str, 
                              whatsapp_client: Union[int, str] = None, msg_type: Union[int, str] = 0,
                              file_url: str = None, file_name: str = None, img_url: str = None,
                              file_path: str = None, webhook: str = None, 
                              expire_after_seconds: int = None) -> Dict:
        """
        Send a WhatsApp message to a WhatsApp group.
        
        Args:
            group_name: Name of the WhatsApp group to send message to
            msg: Message content
            whatsapp_client: Specific WhatsApp client ID to use
            msg_type: Message type (0=text, 1=image, 2=file)
            file_url: URL of a file to send (use for msg_type=2)
            file_name: Name for the file (required for msg_type=2)
            img_url: URL of an image to send (use for msg_type=1)
            file_path: Path to a local file to upload (alternative to file_url/img_url)
            webhook: Webhook URL for delivery notifications
            expire_after_seconds: Time after which the message expires if not delivered
            
        Returns:
            Message sending result with message ID
        """
        data = {
            "group_name": group_name,
            "msg": msg,
            "msg_type": msg_type
        }
        
        # Add optional parameters if provided
        if whatsapp_client:
            data["whatsapp_client"] = whatsapp_client
        if webhook:
            data["webhook"] = webhook
        if expire_after_seconds:
            data["expire_after_seconds"] = expire_after_seconds
            
        files = None
        
        # Handle message type and related parameters
        msg_type = str(msg_type)
        if msg_type == "1":  # Image message
            if img_url:
                data["img_url"] = img_url
            elif file_path and os.path.exists(file_path):
                files = {'file': open(file_path, 'rb')}
            else:
                raise ValueError("For image messages (msg_type=1), either img_url or file_path must be provided")
                
        elif msg_type == "2":  # File message
            if file_name:
                data["file_name"] = file_name
            elif file_path:
                # Extract filename from path if not provided
                data["file_name"] = os.path.basename(file_path)
                
            if file_url:
                data["file_url"] = file_url
            elif file_path and os.path.exists(file_path):
                files = {'file': open(file_path, 'rb')}
            else:
                raise ValueError("For file messages (msg_type=2), either file_url or file_path must be provided")
            
        return self._make_request("POST", "/send_msg/group/", data, files)
    
    def send_bulk_messages(self, phones: List[str], msg: str, country_code: str = None, 
                          whatsapp_client: Union[int, str] = None, msg_type: Union[int, str] = 0,
                          file_url: str = None, file_name: str = None, img_url: str = None,
                          file_path: str = None, webhook: str = None, 
                          expire_after_seconds: int = None) -> Dict:
        """
        Send a WhatsApp message to multiple individual recipients (not a WhatsApp group).
        
        Note:
            This method sends the same message to multiple individual recipients.
            To send a message to a WhatsApp group, use send_message_to_group() instead.
        
        Args:
            phones: List of recipient phone numbers
            msg: Message content
            country_code: Country code (e.g., "91" for India)
            whatsapp_client: Specific WhatsApp client ID to use
            msg_type: Message type (0=text, 1=image, 2=file)
            file_url: URL of a file to send (use for msg_type=2)
            file_name: Name for the file (required for msg_type=2)
            img_url: URL of an image to send (use for msg_type=1)
            file_path: Path to a local file to upload (alternative to file_url/img_url)
            webhook: Webhook URL for delivery notifications
            expire_after_seconds: Time after which the message expires if not delivered
            
        Returns:
            Message sending result with message IDs
        """
        data = {
            "phones": ",".join(phones) if isinstance(phones, list) else phones,
            "msg": msg,
            "msg_type": msg_type
        }
        
        # Add optional parameters if provided
        if country_code:
            data["country_code"] = country_code
        if whatsapp_client:
            data["whatsapp_client"] = whatsapp_client
        if webhook:
            data["webhook"] = webhook
        if expire_after_seconds:
            data["expire_after_seconds"] = expire_after_seconds
            
        files = None
        
        # Handle message type and related parameters
        msg_type = str(msg_type)
        if msg_type == "1":  # Image message
            if img_url:
                data["img_url"] = img_url
            elif file_path and os.path.exists(file_path):
                files = {'file': open(file_path, 'rb')}
            else:
                raise ValueError("For image messages (msg_type=1), either img_url or file_path must be provided")
                
        elif msg_type == "2":  # File message
            if file_name:
                data["file_name"] = file_name
            elif file_path:
                # Extract filename from path if not provided
                data["file_name"] = os.path.basename(file_path)
                
            if file_url:
                data["file_url"] = file_url
            elif file_path and os.path.exists(file_path):
                files = {'file': open(file_path, 'rb')}
            else:
                raise ValueError("For file messages (msg_type=2), either file_url or file_path must be provided")
            
        return self._make_request("POST", "/send_msg/multi/", data, files)
    
    def schedule_message(self, phone: str, msg: str, schedule_time: str,
                        country_code: str = None, whatsapp_client: Union[int, str] = None, 
                        msg_type: Union[int, str] = 0, file_url: str = None, 
                        file_name: str = None, img_url: str = None,
                        file_path: str = None, webhook: str = None) -> Dict:
        """
        Schedule a WhatsApp message for future delivery.
        
        Args:
            phone: Recipient's phone number
            msg: Message content
            schedule_time: When to send (ISO format: YYYY-MM-DD HH:MM:SS)
            country_code: Country code (e.g., "91" for India)
            whatsapp_client: Specific WhatsApp client ID to use
            msg_type: Message type (0=text, 1=image, 2=file)
            file_url: URL of a file to send (use for msg_type=2)
            file_name: Name for the file (required for msg_type=2)
            img_url: URL of an image to send (use for msg_type=1)
            file_path: Path to a local file to upload (alternative to file_url/img_url)
            webhook: Webhook URL for delivery notifications
            
        Returns:
            Message scheduling result with message ID
        """
        # Parse schedule_time into date and time components
        if " " in schedule_time:
            date_part, time_part = schedule_time.split(" ", 1)
        else:
            raise ValueError("schedule_time must be in 'YYYY-MM-DD HH:MM:SS' format")
        
        data = {
            "phone": phone,
            "msg": msg,
            "date": date_part,
            "time": time_part,
            "timezone": "UTC",  # Default to UTC
            "msg_type": msg_type
        }
        
        # Add optional parameters if provided
        if country_code:
            data["country_code"] = country_code
        if whatsapp_client:
            data["whatsapp_client"] = whatsapp_client
        if webhook:
            data["webhook"] = webhook
            
        files = None
        
        # Handle message type and related parameters
        msg_type = str(msg_type)
        if msg_type == "1":  # Image message
            if img_url:
                data["img_url"] = img_url
            elif file_path and os.path.exists(file_path):
                files = {'file': open(file_path, 'rb')}
            else:
                raise ValueError("For image messages (msg_type=1), either img_url or file_path must be provided")
                
        elif msg_type == "2":  # File message
            if file_name:
                data["file_name"] = file_name
            elif file_path:
                # Extract filename from path if not provided
                data["file_name"] = os.path.basename(file_path)
                
            if file_url:
                data["file_url"] = file_url
            elif file_path and os.path.exists(file_path):
                files = {'file': open(file_path, 'rb')}
            else:
                raise ValueError("For file messages (msg_type=2), either file_url or file_path must be provided")
            
        return self._make_request("POST", "/schedule_msg/", data, files)
    
    def cancel_message(self, msg_id: Union[int, str]) -> Dict:
        """
        Cancel a scheduled or pending message.
        
        Args:
            msg_id: Unique Message ID from Send or Schedule message API
            
        Returns:
            Dict containing:
                message (str): Status of the request
                status (int): 0 for error, 1 for success
                
        Example:
            >>> client = WbizToolClient(api_key="your_api_key", client_id=123)
            >>> result = client.cancel_message(msg_id=456)
            >>> print(result)
            {'message': 'Message cancelled successfully', 'status': 1}
        """
        data = {
            "msg_id": msg_id
        }
            
        return self._make_request("POST", "/cancel_msg/", data)
    
    def get_message_status(self, msg_id: Union[int, str]) -> Dict:
        """
        Get the delivery status of a message.
        
        Args:
            msg_id: ID of the message
            
        Returns:
            Dict containing:
                message (str): Status message (e.g., 'connected')
                status (int): Status code (0=error, 1=sent, 2=failed, 3=cancelled, 4=expired)
                status_text (str): Human-readable status description
                error (str): Error message if any
                
        Example:
            >>> client = WbizToolClient(api_key="your_api_key", client_id=123)
            >>> result = client.get_message_status(msg_id=456)
            >>> print(f"Message status: {result.get('status_text', '')}")
        """
        return self._make_request("POST", f"/message/status/{msg_id}/")
    
    def get_messages_report(self, start_date: str, end_date: str, 
                           whatsapp_client: Union[int, str] = None, page: int = 1) -> Dict:
        """
        Get a history report of sent messages.
        
        Args:
            start_date: Start date in DD-MM-YYYY format
            end_date: End date in DD-MM-YYYY format
            whatsapp_client: Optional WhatsApp Client ID to get history for. If not provided, returns messages from all clients.
            page: Page number for pagination (max 200 results per page)
            
        Returns:
            Dict containing:
                message (str): Status of the request
                total (int): Total count of messages in the given period
                status (int): 0 for error, 1 for success
                history (list): List of message objects in the given period
                
        Example:
            >>> client = WbizToolClient(api_key="your_api_key", client_id=123)
            >>> result = client.get_messages_report(
            ...     start_date="01-05-2023",
            ...     end_date="31-05-2023",
            ...     whatsapp_client=456,
            ...     page=1
            ... )
            >>> print(f"Found {result['total']} messages")
            Found 232 messages
        """
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "page": page
        }
        
        if whatsapp_client:
            data["whatsapp_client"] = whatsapp_client
            
        return self._make_request("POST", "/report/", data)
    
    def get_whatsapp_client_status(self, whatsapp_client_id: Union[int, str] = None) -> Dict:
        """
        Get status of WhatsApp clients.
        
        Args:
            whatsapp_client_id: Optional ID of a specific WhatsApp client to check. 
                              If not provided, returns status for all clients.
            
        Returns:
            WhatsApp client status information
        """
        data = {}
        if whatsapp_client_id:
            data["whatsapp_client"] = whatsapp_client_id
            
        return self._make_request("POST", "/whatsapp-client/status/", data)
    
    def get_specific_whatsapp_client_status(self, whatsapp_client_id: Union[int, str]) -> Dict:
        """
        Get status of a specific WhatsApp client.
        
        Note:
            This is an alias for get_whatsapp_client_status(whatsapp_client_id).
        
        Args:
            whatsapp_client_id: ID of the WhatsApp client to check
            
        Returns:
            Status information for the specific client
        """
        return self.get_whatsapp_client_status(whatsapp_client_id)
    
    def list_whatsapp_clients(self) -> Dict:
        """
        List all WhatsApp clients associated with your account.
        
        Returns:
            Dict containing:
                message (str): Status of the request
                status (int): 0 for error, 1 for success
                whatsapp_clients (list): Array of WhatsApp clients with their details
                    Each client contains:
                    - whatsapp_client_id (int): ID of the WhatsApp client
                    - whatsapp_client_number (str): Phone number of the WhatsApp client
                    - is_connected (bool): Connection status of the client
                
        Example:
            >>> client = WbizToolClient(api_key="your_api_key", client_id=123)
            >>> result = client.list_whatsapp_clients()
            >>> for wa_client in result.get('whatsapp_clients', []):
            ...     print(f"Client ID: {wa_client['whatsapp_client_id']}, Connected: {wa_client['is_connected']}")
        """
        return self._make_request("POST", "/whatsapp-client/list/")
    
    def create_whatsapp_client(self, whatsapp_number: str, webhook_url: str) -> Dict:
        """
        Create a new WhatsApp client.
        
        Note:
            This feature requires an Advanced Plan subscription.
        
        Args:
            whatsapp_number: Phone number for the WhatsApp client server
            webhook_url: Webhook URL where JSON data will be posted about events
                      ("qr-generated", "connected", "logged-out") with "whatsapp_client_id"
            
        Returns:
            Dict containing:
                message (str): Status of the request
                status (int): 0 for error, 1 for success
                whatsapp_client_id (int): ID for the created WhatsApp client instance
                
        Example:
            >>> client = WbizToolClient(api_key="your_api_key", client_id=123)
            >>> result = client.create_whatsapp_client(
            ...     whatsapp_number="12345678901",
            ...     webhook_url="https://your-webhook.com/whatsapp-events"
            ... )
            >>> print(f"New WhatsApp client created with ID: {result['whatsapp_client_id']}")
        """
        data = {
            "whatsapp_number": whatsapp_number,
            "webhook_url": webhook_url
        }
            
        return self._make_request("POST", "/whatsapp-client/create/", data) 