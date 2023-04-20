# Проект создания укороченных ссылок

[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

## Описание проекта

Проект позволяет используя оригинальную ссылку сформировать укороченную и сохранить ее в базу данных, также реализован API.

**Используемые технологии**

- Python
- Flask

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Filin1985/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

- Если у вас Linux/macOS

  ```
  source venv/bin/activate
  ```

- Если у вас windows

  ```
  source venv/scripts/activate
  ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

2. База данных и переменные окружения

В проекте используется база данных SQLite

Пример заполнения файла .env

```
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///yacut_db.sqlite3
SECRET_KEY='Ваш секретный ключ'
```

3. Запуск проекта

Создаем базу данных

```
flask db upgrade
```

Запускаем проект

```
flask run
```

Открываем приложение по адресу

[http://localhost:5000/](http://localhost:5000/)

http://localhost:5000/

4. API

Эндпоинты:

```
"/api/id/"
"/api/id/{short_id}/"
```

Запросы:

- Получение оригинального url по короткой ссылке:

```
Method: GET
Endpoint: "/api/id/{short_id}/"
```

- Создание короткой ссылки:

```
Method: POST
Endpoint: "/api/id/"
Payload:
{
    "url": "string",
    "custom_id": "string",
}
```

** Автор [Марат Ихсанов](https://github.com/Filin1985)**
