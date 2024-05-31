# whatsapp-api-webhook-server-python-v2

![](https://img.shields.io/badge/license-CC%20BY--ND%204.0-green)
![](https://img.shields.io/pypi/status/whatsapp-api-webhook-server-python-v2)
![](https://img.shields.io/pypi/pyversions/whatsapp-api-webhook-server-python-v2)
![](https://img.shields.io/pypi/dm/whatsapp-api-webhook-server-python-v2)

## Поддержка

[![Support](https://img.shields.io/badge/support@green--api.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:support@green-api.com)
[![Support](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/greenapi_support_ru_bot)
[![Support](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/79993331223)

## Руководства и новости

[![Guides](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)](https://www.youtube.com/@green-api)
[![News](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/green_api)
[![News](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://whatsapp.com/channel/0029VaHUM5TBA1f7cG29nO1C)

`whatsapp-api-webhook-server-python-v2` - библиотека для получения и обработки вебхуков из мессенджера WhatsApp через API сервиса [green-api.com](https://green-api.com/), в основе которой лежит `FastAPI` сервер.

Чтобы воспользоваться библиотекой, нужно получить регистрационный токен
и ID аккаунта в [личном кабинете](https://console.green-api.com/).
Для разработки можно воспользоваться бесплатным аккаунтом с тарифом "Разработчик".

## API

Документация к REST API находится по [ссылке](https://green-api.com/docs/api/).
Библиотека является оберткой к REST API, поэтому документация по ссылке выше применима и к самой библиотеке.

## Авторизация

Чтобы отправить сообщение или выполнить другие методы Green API, аккаунт WhatsApp в приложении телефона должен быть в авторизованном состоянии. Для авторизации аккаунта перейдите в [личный кабинет](https://console.green-api.com/) и сканируйте QR-код с использованием приложения WhatsApp.

## Примеры подготовки среды

### Пример подготовки среды для Ubuntu Server

#### Обновление системы

Обновим систему:

```shell
sudo apt update
sudo apt upgrade -y
```

#### Брандмауэр

Настроим брандмауэр:

Разрешим соединение по SSH:

```shell
sudo ufw allow ssh
```

Базовые правила:

```shell
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

Разрешаем соединения по HTTP и HTTPS:

```shell
sudo ufw allow http
sudo ufw allow https
```

Активируем брандмауэр:

```shell
sudo ufw enable
```

#### Установка

Необходимо установить систему управления пакетами:

```shell
sudo apt install python3-pip
```

Установка библиотеки:

```shell
python3 -m pip install whatsapp-api-webhook-server-python-v2
```

В качестве примера вы можете скачать и запустить [наш скрипт](https://github.com/green-api/whatsapp-api-webhook-server-python-v2/blob/master/examples/receive_all_with_counter.py). Скрипт отправляет в консоль все входящие уведомления.

```shell
wget https://raw.githubusercontent.com/green-api/whatsapp-api-webhook-server-python-v2/master/examples/receive_all_with_counter.py
```


```shell
python3 -m receive_all_with_counter.py
```

### Пример подготовки среды для Windows Server

#### Установка Python

На сервере должен быть установлен Python. [Инструкция по установке Python](https://www.python.org/downloads/).

#### Как настроить конфигурацию веб-сервера

Для использования IIS (Internet Information Services) в качестве веб-сервера требуется настроить файл
конфигурации `web.config`, чтобы служба IIS могла правильно выполнять код Python. Этот файл располагается в папке
публикации вашего веб-сервера.

После установки интерпретатора следует указать обработчик HttpPlatform в файле `web.config`. Этот обработчик будет
передавать подключения в автономный процесс Python.

Пример конфигурационного файла:

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
    <system.webServer>
        <handlers>
            <add name="PythonHandler" path="*" verb="*" modules="httpPlatformHandler" resourceType="Unspecified"/>
        </handlers>
        <httpPlatform arguments="<Path-to-server-file>\receive_all_with_counter.py.py"
                      processesPerApplication="16"
                      processPath="<Path-to-python>\python.exe"
                      startupTimeLimit="60"
                      stdoutLogEnabled="true"
                      stdoutLogFile="<Path-to-log-file>\python.log">
            <environmentVariables>
                <environmentVariable name="SOME_VARIABLE" value="%SOME_VAR%"/>
            </environmentVariables>
        </httpPlatform>
    </system.webServer>
</configuration>
```

- `<Path-to-python>` - путь к исполняемому файлу интерпретатора Python;
- `<Path-to-server-file>` - путь к исполняемому файлу сервера (например, receive_all_with_counter.py из примера);
- `<Path-to-log-file>` - путь к файлу логов.

Также потребуется открыть соответствующий порт во внешнюю сеть, установив настройки брандмауэра (дополнительные
параметры -> Правила для входящих подключений -> Создать правило -> Тип правила = Порт, Протоколы и порт -> TCP, указать
порт, Действие -> Разрешить соединение).

### Запуск примера сервера с помощью Docker

На машине должен быть установлен Docker.

Чтобы получить образ из Docker Hub, нужно написать команду:

```
sudo docker pull greenapi/whatsapp-api-webhook-server-python-v2
```

Запустим образ в контейнере с указанием порта и отображением консоли:

```
sudo docker run -it -e PORT=8000 -p 80:8000 greenapi/whatsapp-api-webhook-server-python-v2
```

В данном случае webhook-сервер запускается на `8000` порту внутри контейнера и проксируется на `80` порт машины, на которой запускается контейнер

В [личном кабинете](https://console.green-api.com/) необходимо необходимо указать IP (или домен) с этим (`80`) портом.

После старта контейнера в консоли будут доступны данные входящих вебхуков

Также можно запустить пример с помощью `docker compose` (из корневой директории репозитория):

```
docker compose up --build
```

## Запуск сервера

Для использования в ваших решениях, импортируйте `GreenAPIWebhookServer` класс и иницализируйте объект сервера:

```python
from whatsapp_api_webhook_server_python_v2.main import GreenAPIWebhookServer

def event_handler(webhook_type: str, webhook_data: dict):
    # Пример функции, в которой необходимо
    # разместить вашу логику обработки
    ...

handler = GreenAPIWebhookServer(
    event_handler=event_handler,    # Функция обработки вебхуков (см. examples)
    host="0.0.0.0",                 # Ваш хост
    port=8080,                      # Ваш порт
    webhook_auth_header=None,       # Ожидаемый заголовок авторизации (см. личный кабинет)
)

if __name__ == "__main__":
    handler.start()
```

Параметр `event_handler` это ваша функция, которая должна обрабатывать входящие вебхуки.

Аргументы, которые должны быть реализованы в функции:

| Аргумент            | Описание                 |
|---------------------|--------------------------|
| `webhook_type: str` | Тип входящего вебхука    |
| `webhook_data: dict`| Данные вебхука           |

Пример: [receive_all_with_counter.py](https://github.com/green-api/whatsapp-api-webhook-server-python-v2/blob/master/examples/receive_all_with_counter.py).

Также, если есть необходимость реализовать обарботку входящих данных самостоятельно, вы можете использовать `Pydantic v2` модели, которые находятся в файле `webhook_dto.py`

## Как перенаправить входящие уведомления на веб-сервер

Чтобы перенаправить входящие уведомления, нужно в [личном кабинете](https://console.green-api.com/) установить адрес отправки уведомлений (URL).

## Документация по методам сервиса

[Документация по методам сервиса](https://green-api.com/docs/api/)

## Лицензия

Лицензировано на условиях [
Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)
](https://creativecommons.org/licenses/by-nd/4.0/). [LICENSE](../LICENSE).
