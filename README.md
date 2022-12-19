
# Telegram To Do Bot

The bot helps you with managing a single To Do list.

The bot is asyncronous thanks to [aiogram](https://github.com/aiogram/aiogram) and [aredis-om for Python](https://github.com/redis/redis-om-python).

## Setup
Add `.env` file with settings
```
TODO_BOT_TELEGRAM_BOT_TOKEN=your token
TODO_BOT_MAX_TASK_LENGTH=200
TODO_BOT_MAX_TASKS_IN_LIST=1000

REDIS_PASSWORD=your password
```

## Build and run

```
docker compose build
docker compose up
```
