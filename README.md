# CLI

### Требования

* Python 3.8
* Вызов внешних команд на Windows работает некорректно

### Установка зависимостей

```shell
pip install -r requirements.txt
```

### Запуск

```shell
python main.py
```

### Разработка

- Установить `pre-commit`:

```shell
pre-commit install
```

- Отформатировать код:

```shell
pre-commit run --all-files
```

- Запуск тестов
```shell
pytest tests/
```
