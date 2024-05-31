FROM python:3.11-slim
LABEL maintainer="Green API <support@green-api.com>"

COPY ./requirements.txt /requirements.txt
COPY ./README.md /README.md
COPY ./setup.py /setup.py
COPY ./whatsapp_api_webhook_server_python_v2 /whatsapp_api_webhook_server_python_v2
COPY ./examples /examples

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install -e .

CMD ["python3", "examples/docker_example.py"]
