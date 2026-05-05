# Quick Start Guide

## Быстрая установка и запуск

### 1. Настройка окружения

```bash
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_LLM_MODEL=gpt-4-turbo-preview
WORKSPACE_PATH=/workspace
OPENHANDS_API_KEY=your_openhands_or_llm_key
OPENHANDS_MODEL=openhands/claude-sonnet-4-5-20250929
OPENHANDS_LLM_BASE_URL=
TESTER_COMMAND=pytest -q
```

### 2. Запуск через Docker (рекомендуется)

```bash
docker compose up --build
```

Сервер запустится на `http://localhost:8000`

### 3. Локальный запуск (опционально)

```bash
pip install -r requirements.txt
python main.py
```

### 4. Проверка работоспособности

Откройте в браузере: `http://localhost:8000/docs` для интерактивной документации API

Или используйте curl:

```bash
curl http://localhost:8000/health
```

### 5. Примеры использования

#### Текстовый запрос

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is artificial intelligence?"}'
```

### 6. Использование Python скрипта

```bash
python example_usage.py
```

## Архитектура потока выполнения

1. **User** отправляет запрос через API Gateway
2. **Router Agent** направляет запрос в pipeline
3. **Architect Agent** формирует план реализации
4. **Coding Agent (OpenHands)** выполняет coding-этап в общей директории
5. **Tester Agent** запускает тесты в той же общей директории
6. **Critic Agent** проверяет качество ответа
7. **Aggregation** объединяет результаты
8. **User** получает финальный ответ

## Настройка компонентов


### OpenHands SDK и shared workspace

Все этапы coding/testing работают через общий Docker volume, смонтированный как `/workspace`.
Настройка через `.env`:
```env
WORKSPACE_PATH=/workspace
OPENHANDS_API_KEY=your_openhands_or_llm_key
OPENHANDS_MODEL=openhands/claude-sonnet-4-5-20250929
OPENHANDS_LLM_BASE_URL=
TESTER_COMMAND=pytest -q
```

## Troubleshooting

### Ошибка импорта модулей

Убедитесь, что все зависимости установлены:
```bash
pip install -r requirements.txt
```

### Ошибка API ключа

Проверьте, что файл `.env` создан и содержит правильный `OPENAI_API_KEY`



## Следующие шаги

1. Настройте агентов под ваши задачи
2. Расширьте систему новыми инструментами или агентами
3. Настройте мониторинг и логирование

