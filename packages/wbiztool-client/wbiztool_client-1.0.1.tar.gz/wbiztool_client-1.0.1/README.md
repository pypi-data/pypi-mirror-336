# WbizTool Client

A Python client library for the [WbizTool](https://wbiztool.com) API, making it easy to integrate WhatsApp messaging capabilities into your Python applications.

## About WbizTool

[WbizTool](https://wbiztool.com) is a powerful platform that provides WhatsApp API integration for businesses. With WbizTool, you can automate your WhatsApp messaging workflow and engage with your customers more effectively.

Visit [wbiztool.com](https://wbiztool.com) to create an account and get your API credentials.

## Installation

```bash
pip install wbiztool-client
```

## Authentication

You'll need an API key and client ID from your [WbizTool account](https://wbiztool.com/login):

1. Log in to your WbizTool account
2. Go to API Keys section
3. Generate a new API key if you don't have one

### Using Environment Variables

You can set your credentials as environment variables:

```bash
export WBIZTOOL_API_KEY=your_api_key
export WBIZTOOL_CLIENT_ID=your_client_id
```

The client will automatically use these variables if not provided explicitly during initialization.

## Quick Start

```python
from wbiztool_client import WbizToolClient

# Option 1: Initialize with explicit credentials
client = WbizToolClient(
    api_key='your_api_key',
    client_id='your_client_id'  # Optional, can be provided with each request
)

# Option 2: Initialize using environment variables
client = WbizToolClient()  # Will use WBIZTOOL_API_KEY and WBIZTOOL_CLIENT_ID

# Option 3: Initialize and validate credentials immediately
try:
    client = WbizToolClient(validate_credentials=True)
    print("Credentials are valid!")
except ValueError as e:
    print(f"Invalid credentials: {e}")

# Check if API is operational
status = client.health_check()
print(status)

# Send a simple text message
response = client.send_message(
    phone='919876543210',  # Include country code
    msg='Hello from Python!',
    msg_type=0  # 0 for text message
)
print(response)
```

## Features

- Send text messages
- Send image messages with captions
- Send document/file messages with captions
- Upload files directly from your local system
- Send messages to multiple individual recipients
- Send messages to WhatsApp groups
- Schedule messages for future delivery
- Cancel scheduled messages
- Check message delivery status
- Get reports of sent messages
- Manage WhatsApp clients

## API Methods

### Authentication and Status

- `health_check()` - Check if the API is operational
- `check_credentials()` - Verify API credentials

### Messaging

- `send_message(phone, msg, ...)` - Send a WhatsApp message to an individual
- `send_message_to_group(group_name, msg, ...)` - Send a message to a WhatsApp group
- `send_bulk_messages(phones, msg, ...)` - Send to multiple individual recipients
- `schedule_message(phone, msg, schedule_time, ...)` - Schedule a message
- `cancel_message(msg_id)` - Cancel a scheduled message
- `get_message_status(msg_id)` - Get delivery status

### Reporting

- `get_messages_report(start_date, end_date, ...)` - Get sent messages report

### WhatsApp Clients

- `get_whatsapp_client_status(whatsapp_client_id=None)` - Get status of all WhatsApp clients or a specific client
- `get_specific_whatsapp_client_status(whatsapp_client_id)` - Alias for checking a specific client status
- `list_whatsapp_clients()` - List all WhatsApp clients
- `create_whatsapp_client(whatsapp_number, webhook_url)` - Create a new WhatsApp client (Advanced Plan required)

## Examples

### Sending a Text Message

```python
response = client.send_message(
    phone='919876543210',
    msg='Hello, this is a simple text message',
    country_code='91',
    msg_type=0,  # 0 for text
    webhook='https://your-webhook.com/callback'  # Optional webhook for delivery notifications
)
```

### Sending an Image with Caption

```python
# Using an image URL
response = client.send_message(
    phone='919876543210',
    msg='Check out this image!',
    country_code='91',
    msg_type=1,  # 1 for image
    img_url='https://example.com/path/to/image.jpg'
)

# OR upload a local image file
response = client.send_message(
    phone='919876543210',
    msg='Check out this image!',
    country_code='91',
    msg_type=1,  # 1 for image
    file_path='/path/to/local/image.jpg'
)
```

### Sending a Document/File with Caption

```python
# Using a file URL
response = client.send_message(
    phone='919876543210',
    msg='Please see the attached document',
    country_code='91',
    msg_type=2,  # 2 for document/file
    file_url='https://example.com/path/to/document.pdf',
    file_name='Important Document.pdf'
)

# OR upload a local file
response = client.send_message(
    phone='919876543210',
    msg='Please see the attached document',
    country_code='91',
    msg_type=2,  # 2 for document/file
    file_path='/path/to/local/document.pdf'
)
```

### Message with Expiry Time

```python
# Message will expire if not delivered within 1 hour (3600 seconds)
response = client.send_message(
    phone='919876543210',
    msg='This message will expire if not delivered within 1 hour',
    country_code='91',
    expire_after_seconds=3600
)
```

### Sending a Message to a WhatsApp Group

```python
# Send a text message to a WhatsApp group
response = client.send_message_to_group(
    group_name='Family Group',
    msg='Hello everyone in the group!',
    msg_type=0  # 0 for text
)

# Send a document to a WhatsApp group
response = client.send_message_to_group(
    group_name='Work Team',
    msg='Here is the report for everyone',
    msg_type=2,  # 2 for document/file
    file_url='https://example.com/path/to/report.pdf',
    file_name='Team Report.pdf'
)
```

### Sending to Multiple Individual Recipients

```python
# Send the same message to multiple phone numbers
response = client.send_bulk_messages(
    phones=['919876543210', '919876543211', '919876543212'],
    msg='This message goes to multiple individuals',
    country_code='91',
    msg_type=0  # 0 for text
)
```

### Checking WhatsApp Client Status

```python
# Get status of all WhatsApp clients
all_clients_status = client.get_whatsapp_client_status()
print(all_clients_status)

# Get status of a specific WhatsApp client
specific_client_status = client.get_whatsapp_client_status(whatsapp_client_id=123)
# Or using the alias method
specific_client_status = client.get_specific_whatsapp_client_status(whatsapp_client_id=123)
print(specific_client_status)
```

### Scheduling a Message

```python
from datetime import datetime, timedelta

# Schedule for 1 hour from now
schedule_time = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')

response = client.schedule_message(
    phone='919876543210',
    msg='This is a scheduled message',
    schedule_time=schedule_time,
    country_code='91'
)
```

### Getting Message Reports

```python
# Get message history for a specific date range
report = client.get_messages_report(
    start_date='01-05-2023',  # DD-MM-YYYY format
    end_date='31-05-2023',    # DD-MM-YYYY format
    whatsapp_client=123,      # Optional: specific WhatsApp client ID
    page=1                    # For pagination
)

# Print the total count of messages
print(f"Found {report['total']} messages")

# Process the message history
for message in report.get('history', []):
    print(f"Message {message['id']}: {message['message_status']}")
```

### Canceling a Message

```python
# Cancel a scheduled or pending message
result = client.cancel_message(msg_id=123)
if result['status'] == 1:
    print("Message canceled successfully")
else:
    print(f"Failed to cancel message: {result['message']}")
```

### Creating a WhatsApp Client

```python
# Create a new WhatsApp client (Advanced Plan required)
result = client.create_whatsapp_client(
    whatsapp_number='919876543210', 
    webhook_url='https://your-webhook.com/whatsapp-events'
)

if result['status'] == 1:
    print(f"New WhatsApp client created with ID: {result['whatsapp_client_id']}")
else:
    print(f"Failed to create WhatsApp client: {result['message']}")
```

### Listing WhatsApp Clients

```python
# Get all WhatsApp clients for your account
result = client.list_whatsapp_clients()

if result['status'] == 1:
    for client in result.get('whatsapp_clients', []):
        print(f"Client ID: {client['whatsapp_client_id']}")
        print(f"Number: {client['whatsapp_client_number']}")
        print(f"Connected: {client['is_connected']}")
        print("---")
else:
    print(f"Failed to list WhatsApp clients: {result['message']}")
```

### Checking if credentials are valid at any time

```python
# Check if credentials are valid at any time
try:
    result = client.check_credentials()
    print("Credentials are valid!")
except ValueError as e:
    print(f"Credential error: {e}")
```

## Additional Resources

- [WbizTool Official Website](https://wbiztool.com)
- [API Documentation](https://wbiztool.com/docs)
- [Support](https://wbiztool.com/contact)

## License

MIT License 