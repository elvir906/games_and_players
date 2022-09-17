![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
[![Django](https://img.shields.io/badge/-Django-464646?style=for-the-badge&logo=Django)](https://www.djangoproject.com/)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)

## О проекте
Итак, перед тобой проект, на котором подключены FastAPI и Django одновременно. Django используется только как ORM и админка, FastAPI используется для запросов. Мы не фанаты DRF, почти все проекты пишем в связке какой-то фронт(Vue/React) + API(чаще всего не REST), поэтому использование Class-based Views пригодится максимум для админки. Собственно, от Django кроме ORM и умения рулить админкой мы больше ничего и не берем. Если не сталкивался с FastAPI - не беда, наверняка ты уже пробовал Flask, они очень похожи.

Дисклеймер: не пытайся оценить структуру проекта, это всего лишь тестовое, которое должно решаться парой десятков строк кода.

Мы храним базу данных игроков и игр. В игре может быть не более 5 игроков. Игроки и игры создаются при помощи API-вызовов с применением аутентификации по методу JWT(уже внедрено, читай OpenAPI-документацию доступную по запросу на http://localhost:8000/docs). 

## Инфраструктура
Мы используем активно Docker и Docker-compose для поднятия инфраструктуры, используй их.
`docker-compose up -d` поднимет всю инфраструктуру проекта и проект будет доступен по http://localhost:8000/. Правки применятся автоматически(благодаря --reload(command в docker-compose), файлы внутри контейнеров и на локальной машине синхронизированы через volumes(docker-compose).
Внутрь контейнера с python можно попасть, используя команды:
```
docker ps #отобразит список всех контейнеров
docker exec -ti <container_id> bash #войдет в запущенный контейнер для выполнения команд, например - создания superuser
````

## Задачи в рамках тестового задания:

- [ ] Необходимо отобразить модели игрока и игр в админке (http://localhost:8000/django/admin)

*Задача на понимание моделей Django, миграциями, работы с админкой и docker*

ТЗ: отобразить в списке игроков: имя, email, дату и время создания игрока, дату и время изменения игрока(в нашем случае только через админку); добавить поиск по имени или email. Отобразить в списке игр название игры и имена игроков через запятую(отдельным столбцом), дату и время создания игры, дату и время изменения игры. На странице редактирования игры отобразить inline'ами всех привязанных игроков.
*Модели менять можно!*

Что будем оценивать:
* создана ли миграция?
* выполнены ли все условия ТЗ?
* как выполнен reverse lookup?

- [ ] Задваивание игроков с одинаковым name и email

*Задача на понимание FastAPI, валидации и транзакций*

ТЗ: при создании игрока(/new_player) его имя и email должны быть уникальны. Имя должно содержать только цифры от 0 до 9 и только буквы от a до f. 
Если пользователь с таким email и name уже существует, необходимо вернуть ошибку с HTTP-кодом 400, status = "error", текстом "player with such name or email already exists". Аналогичную ошибку необходимо вернуть при ошибки валидации имени пользователя или e-mail'а с указанием соответствующего текста ошибки

Что будем оценивать:
* возможна ли race condition?
* выполнены ли все условия ТЗ?
* можно ли получить 500 ошибку при отправке данных, величина которых не предусмотрена БД?

- [ ] Реализовать логику для метода /add_player_to_game

*Задача на работу с ManyToMany Django ORM, валидацией FastAPI, транзакциями*

ТЗ: при запросе игрок с указанным id должен добавляться в игру с указанным id. Если игрока или игры с заданными id не существует, должна возвращаться ошибка с HTTP-кодом 400, status = "error" и соответствующим текстом. Количество игроков в одной игре не более 5.

Что будем оценивать:
* возможна ли race condition?
* выполнены ли все условия ТЗ?
* можно ли получить 500 ошибку?
* что произойдет при добавлении одного игрока два и более раз?

## Как сдавать тестовое
Перешлите архив с вашими доработками нашему менеджеру, мы дадим ответ на следующий день. Спасибо за внимание ;)





