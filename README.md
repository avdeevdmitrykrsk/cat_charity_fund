# Данный проект представляет из себя Благотворительный Фонд поддержки котиков! Если ваш котик захворал, а вы так и не успели получить новую профессию на платформе [ЯндексПрактикум](https://practicum.yandex.ru/) и не можете позволить себе оплатить лечение вашему питомцу - не беда! Для этого заполните форму обратной связи на сайте [QRKot](https://github.com/avdeevdmitrykrsk/) и наши специалисты создадут новый фонд для вас! Если же вы настолько альтруистичен, что готовы отдать свои кровные "5 копеек", то переходите на сайт [QRKot](https://github.com/avdeevdmitrykrsk/), зарегистрируйтесь и внесите пожертвование во славу котикам!!! (не является публичной офертой.)

## Стек:
* python 3.9
* fastapi
* Alembic
* unicorn
* SQLAlchemy

### Клонировать репозиторий и перейти в него в командной строке:

```sh
git clone git@github.com:avdeevdmitrykrsk/cat_charity_fund.git
```

```sh
cd cat_charity_fund
```

### Cоздать и активировать виртуальное окружение:

```sh
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```sh
    source venv/bin/activate
    ```

* Если у вас windows

    ```sh
    source venv/scripts/activate
    ```

### Установить зависимости из файла requirements.txt:

```sh
python3 -m pip install --upgrade pip
```

```sh
pip install -r requirements.txt
```

### Создать файл конфигурации `.env`, пример заполнения можете посмотреть в корневой папке в файле `.env.example`

### Выполнить миграции:
```sh
alembic upgrade head
```

### Запустить виртуальный сервер:
```sh
uvicorn app.main:app
```

# Благотворительный проект.
## Создание благотворительного проекта:
### Доступно только администраторам проекта.
### `post-запрос`
```sh
127.0.0.1:8000/charity_project/
```
```json
{
"name": "string",
"description": "string",
"full_amount": 0
}
```
## Обновление информации о проекте:
### Доступно только администраторам проекта. Нельзя указать full_amount меньше чем уже есть в invested_amount
### `patch-запрос`
```sh
127.0.0.1:8000/charity_project/<id>
```
```json
{
"name": "string",
"description": "string",
"full_amount": 0
}
```

## Удаление проекта:
### Доступно только администраторам проекта. Нельзя удалить проект в который уже задонатили.
### `patch-запрос`
```sh
127.0.0.1:8000/charity_project/<id>
```

## Получение списка всех проектов:
### `get-запрос`
```sh
127.0.0.1:8000/charity_project/
```

# Пожертвование.
## Создание пожертвования:
### Доступно только зарегестрированному пользователю.
### `post-запрос`
```sh
127.0.0.1:8000/donation/
```
```json
{
"full_amount": 0,
"comment": "string"
}
```
## Получение списка всех пожертвований:
### Доступно только администраторам проекта.
### `get-запрос`
```sh
127.0.0.1:8000/donation/
```

## Получение списка пожертвований пользователя, выполняющего запрос:
### Доступно только зарегестрированному пользователю.
```sh
127.0.0.1:8000/donation/my
```
```json
[
{
"full_amount": 0,
"comment": "string",
"id": 0,
"create_date": "2019-08-24T14:15:22Z"
}
]
```

## Получение отчета о закрытых проектах:
### Доступно только администратору.
### 'GET-запрос'
```sh
127.0.0.1:8000/google
```


### `Redoc`-документация `openapi.json` находится в корневой директории проекта.
### `Swagger` документация доступна по адресу:
```sh
127.0.0.1:8000/docs
```
Автор [GitHub - dmitryavdeevkrsk](https://github.com/avdeevdmitrykrsk/)