from whatsapp_api_webhook_server_python_v2.main import GreenAPIWebhookServer


def pretty_print_status_data(webhook_data: dict):
    instance_data = webhook_data["instance_data"]

    timestamp = webhook_data["timestamp"]
    id_message = webhook_data["id_message"]

    id_instance = instance_data["id_instance"]
    wid = instance_data["wid"]

    pretty_message = (
        "Received status data:\n\n"
        f"Message ID: {id_message}\n"
        f"Timestamp: {timestamp}\n"
        f"Instance ID: {id_instance}\n"
        f"WhatsApp ID: {wid}"
    )

    print(pretty_message)


def event_handler(webhook_type: str, webhook_data: dict):
    if webhook_type == "outgoingMessageStatus":
        pretty_print_status_data(webhook_data)


handler = GreenAPIWebhookServer(
    event_handler=event_handler,
    host="0.0.0.0",
    port=8080,
    webhook_auth_header=None,  # Change it to actual webhook secret
)

if __name__ == "__main__":
    handler.start()
