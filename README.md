# Тестовое задание

Телеграм бот ***TestExchangeRateBot***

## Описание

Всего у бота 4 функции:
 - Обработка стартого запроса */start*
 - Обработка запроса */help* - рассказать пользователю о функциях бота
 - Обработка запроса */convert* - конвертации суммы из одной валюты в одну или несколько.
 - Обработка приветсвия и прощания.

 Есть 3 способа конвертировать сумму:
 - написать полностью запрос - */convert 1000 RUB to USD*
 - написать */convert* - начнется диалог, где бот будет просить дополнить запрос
 - нажать на inline-кнопку - начнется диалог, аналогичный предыдущему


## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/Dermofet/test-easy-byte.git
    ```

2. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```
## Зависимости

- python = 3.12.1
- loguru = 0.7.2
- pydantic = 2.6.1
- pydantic-settings = 2.1.0
- python-dotenv = 1.0.1
- python-telegram-bot = 20.8

## Использование

1. Запустите бота:

    ```bash
    python main.py
    ```

2. Откройте Telegram и найдите бота по его имени или перейдите по [***ссылке***](https://t.me/TestExchangeRateBot).

3. Начните использование бота, следуя инструкциям.

## Структура проекта

В файле *main.py* создается экземпляр телеграм бота и запускается обработка запросов.

В файле *handlers.py* находятся обработчики.

Бизнес-логика вынесена в файл *service.py*.

Текстовые константы вынесены в отдельный файл *answer.py*.

В папке *logger* находится логгер (loguru), настроенный на написание логов как в терминал, так и в файлы.

В папке *settings* находятся конфиги проекта. Конфиги парсятся из *.env* файла.