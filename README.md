from fastapi import APIRouter

# Тестовое задание в WhyNot на позицию Python разработчик

## Задание

Сделать сервис на FastAPI, предоставляющий один метод:\
`GET /test`, который возвращает время затраченное на обработку запроса.

В качестве полезной работы метод спит 3 секунды:

```python
import asyncio

async def work() -> None:
    await asyncio.sleep(3)
```

При этом не допускается одновременная работа нескольких функций `work()`

В качестве ответа метод возвращает фактически затраченное время на обработку запроса:

```python
from pydantic import BaseModel
from fastapi import APIRouter

from time import monotonic

class TestResponse(BaseModel):
    elapsed: float

router = APIRouter()

@router.get("/test", response_model=TestResponse)
async def handler() -> TestResponse:
    ts1 = monotonic()
    # ... организация вызовы функции work() ...
    ts2 = monotonic()
    
    return TestResponse(elapsed=ts2 - ts1)
```

Тестирование:\
Метод считается успешным, если при одновременном вызове каждый возвращающийся
ответ содержит elapsed отличающийся от предыдущего не менее чем на 3 секунды


## Решение

### Запуск

Для запуска понадобятся:
- `Python 3.10+`
- `Poetry`

Для установки зависимостей: `poetry install`

Для запуска: `poetry run main.py`

API будет доступно на локальной машине по адресу: http://127.0.0.1:8000

### Пояснения к решению

Для обеспечения того, чтобы одновременно не выполнялись несколько вызовов функции `work()`, используется `asyncio.Lock()`.\ 
Этот механизм синхронизации гарантирует, что в каждый момент времени будет выполняться только одна функция `work()`.

Внутри обработчика используется контекстный менеджер `async with work_lock`. 
Он блокирует доступ для всех других вызовов до тех пор, пока текущий вызов не завершит выполнение функции `work()`

Но это работает только в рамках одного потока (Event Loop'а). 
Если мы запустим несколько процессов/потоков (например, через `Gunicorn`), 
то функция `work()` сможет одновременно выполняться в разных потоках/процессах.

Если такое поведение для нас нежелательно, то нужно рассмотреть другие механизмы синхронизации, 
но в ТЗ не указано подробностей по этому поводу)

### Тестирование

К решению написано 2 теста на `Pytest`

Первый тест (`test_single_request`) проверяет работу одного отдельного запроса.

Второй тест (`test_parallel_requests`) проверяет работу уже нескольких запросов одновременно.\
При проверке времени беру `2.9`, а не ровно `3`, потому что по факту время запроса выходит `3` секунды +- несколько миллисекунд.

Чтобы запустить тесты: `poetry run pytest -vv tests.py`\
(Придётся подождать, там выполняется 4 запроса по 3 секунды каждый, а значит прогонка тестов займёт 12+ секунд)


## Контакты
- [Telegram - @printeromg](https://t.me/printeromg)
- [Почта - kitaev.gregory@gmail.com](mailto:kitaev.gregory@gmail.com)
