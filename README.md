# My Movies

My Movies — небольшое приложение для хранения списка фильмов.

В нём можно:
- добавлять фильмы;
- указывать жанр;
- ставить оценку от 1 до 10;
- выбирать статус просмотра.

Все фильмы сохраняются в PostgreSQL, поэтому после обновления страницы они не пропадают.

## Что использовано

- Python + Flask - бэкенд
- HTML, CSS, JavaScript - фронтенд
- PostgreSQL - база данных

## Структура проекта

```text
movie-service/
├── backend/
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── .env.example
├── .gitignore
└── README.md
```

# Как запустить проект

Для запуска должны быть установлены Python и PostgreSQL.

## 1. Скачать проект

Скачать репозиторий с GitHub или выполнить:

```bash
git clone <ссылка на репозиторий>
```

После этого перейти в папку проекта:

```bash
cd movie-service
```

## 2. Создать виртуальное окружение

На macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

На Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

## 3. Установить библиотеки

Выполнить:

```bash
pip install -r backend/requirements.txt
```

Эта команда установит Flask и остальные библиотеки, которые нужны приложению.

## 4. Запустить PostgreSQL

PostgreSQL должен быть установлен и запущен на компьютере.

Нужно открыть PostgreSQL и создать базу данных:

```sql
CREATE DATABASE movies_db;
```

Саму таблицу для фильмов создавать вручную не нужно — приложение создаст её автоматически при первом запуске.

## 5. Настроить подключение к PostgreSQL

В проекте есть файл:

```text
.env.example
```

Нужно создать рядом новый файл с названием:

```text
.env
```

И заполнить его своими данными PostgreSQL:

```env
DB_HOST=localhost
DB_NAME=movies_db
DB_USER=имя_пользователя_postgresql
DB_PASSWORD=пароль
```

Например:

```env
DB_HOST=localhost
DB_NAME=movies_db
DB_USER=postgres
DB_PASSWORD=1234
```

Если у пользователя PostgreSQL нет пароля:

```env
DB_PASSWORD=
```

Файл `.env` у каждого пользователя свой и в GitHub не загружается.

## 6. Запустить приложение

Находясь в папке `movie-service`, выполнить:

```bash
python backend/app.py
```

Если команда `python` не работает, использовать:

```bash
python3 backend/app.py
```

Если всё запустилось правильно, в терминале появится примерно такая строка:

```text
Running on http://127.0.0.1:5000
```

## 7. Открыть сайт

Открыть браузер и перейти по адресу:

```text
http://127.0.0.1:5000
```

Откроется приложение My Movies.

Теперь можно добавить фильм через форму.

Для проверки сохранения данных можно:

1. добавить фильм;
2. обновить страницу;
3. проверить, что фильм остался в списке.

Если фильм после обновления страницы остался, значит он успешно сохранился в PostgreSQL.

## Как остановить приложение

В терминале, где запущен Flask, нажать:

```text
Ctrl + C
```