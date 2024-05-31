import os

from whatsapp_api_webhook_server_python_v2.main import GreenAPIWebhookServer

count = 0

port = int(os.environ.get("PORT", 8080))
auth_header = str(os.environ.get("AUTH_HEADER", None))


def event_handler(webhook_type: str, webhook_data: dict):
    global count
    count += 1
    print(
        f"Recieved webhook: {webhook_type}\n"
        f"Webhooks recieved since start: {count}\n\n"
        f"{webhook_data}\n"
    )


handler = GreenAPIWebhookServer(
    event_handler=event_handler,
    host="0.0.0.0",
    port=port,
    webhook_auth_header=auth_header,  # Change it to actual webhook secret
)


if __name__ == "__main__":
    handler.start()
