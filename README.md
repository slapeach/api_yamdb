# api_yamdb
## **Описание проекта**
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «книги», «фильмы», «музыка». Список категорий расширяется командой.
Проект «YaMDb» реализован на Django, в свою очередь «API для YaMDb» реализован с использованием библиотеки Django REST Framework (DRF).
DRF мощный и гибкий инструмент для построения Web API, который имеет следующие преимущества:
* Крайне удобная для разработчиков браузерная версия API;
* Наличие пакетов для OAuth1a и OAuth2 авторизации;
* Сериализация, поддерживающая ORM и не-ORM источники данных;
* Возможность полной и детальной настройки - можно использовать обычные представления-функции, если вы не нуждаетесь в мощном функционале;
* Расширенная документация и отличная поддержка сообщества.<br/>

Через API Yatube можно публиковать отзывы и делиться своим мнением в комментариях.



## **Как запустить проект**
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/slapeach/api_yamdb.git
```
```
cd api_yamdb
```

Cоздать виртуальное окружение:
```
python3 -m venv env
```
На Windows:
```
python -m venv venv
```
Активировать виртуальное окружение:
```
source env/bin/activate
```
На Windows:
```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
На Windows:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

Выполнить миграции:
```
python3 manage.py migrate
```
На Windows:
```
python manage.py migrate
```

Запустить проект:
```
python3 manage.py runserver
```
На Windows:
```
python manage.py runserver
```


## **Примеры запросов**


**Пример создания нового пользователя**<br/>

Для создания нового пользователя отправьте POST-запрос на .../auth/signup/ с указанием имени пользователя и почты.
После этого на почту придет код подтверждения регистрации.
```
POST /auth/signup/
```
```
{
    "username" : "newuser",
    "email" : "user@yandex.ru"
}
```
<br/>

**Получение JWT-токена**

Для получения JWT-токена необходимо отправить POST-запрос на .../auth/token/ с именем пользователя и кодом, который пришел на почту.
```
POST /auth/token/
```
```
{
    "username" : "newuser",
    "confirmation_code" : "U3FI0MU87"
}
```
Будет получен ответ следующего вида:
```
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjIwODU1Mzc3LCJqdGkiOiJkY2EwNmRiYTEzNWQ0ZjNiODdiZmQ3YzU2Y2ZjNGE0YiIsInVzZXJfaWQiOjF9.eZfkpeNVfKLzBY7U0h5gMdTwUnGP3LjRn5g8EIvWlVg"
}
```
Токен необходим для дальнейшей работы с API для YaMDb. Чтобы обновить токен, необходимо так же отправить запрос POST /auth/token/ с указанием имени пользователя и кодом подтверждения.  
<br/>

**Дополнение информации в профиле**
Для изменения информации о себе необходимо отправть PATCH-запрос на .../users/me/
```
POST /api/v1/users/me/
```
```
{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
}
```
<br/>

**Получение списка категорий**
Вы можете ознакомиться со списком всех категорий произведений, отправив GET-запрос на /api/v1/categories/
```
GET /api/v1/categories/
```
<br/>

**Получение списка жанров**
Также Вы можете ознакомиться со списком всех жанров произведений, отправив GET-запрос на /api/v1/genres/
```
GET /api/v1/genres/
```
<br/>

**Получение списка всех произведений**
Можно получить список всех произведений, отправив GET-запрос на /api/v1/titles/
```
GET /api/v1/titles/
```
<br/>

**Пример добавления нового отзыва**
Отзыв можно отправить на любое произведение, указав его id: /api/v1/titles/{title_id}/reviews/
```
POST /api/v1/titles/{title_id}/reviews/
```
```
{
    "text": "string",
    "score": 1
}
```
<br/>

**Получение списка всех отзывов**

```
GET /api/v1/titles/{title_id}/reviews/
```
<br/>


**Добавления нового комментария к отзыву на произведение**
```
POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
```
{
    "text": "string"
}
```
<br/>

**Получение списка всех комментариев в отзыву**

```
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
<br/>