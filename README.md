# praktikum_new_diplom

Дипломный проект - приложение «Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

# Исходники
Мы подготовили для вас готовый фронтенд и структуру приложения.
В репозитории есть папки frontend, backend, infra, data и docs.
В папке frontend находятся файлы, необходимые для сборки фронтенда приложения.
В папке infra — заготовка инфраструктуры проекта: конфигурационный файл nginx и docker-compose.yml.
В папке backend пусто, там вы будете с нуля разрабатывать бэкенд продуктового помощника.
В папке data подготовлен список ингредиентов с единицами измерения. Список сохранён в форматах JSON и CSV: данные из списка будет необходимо загрузить в базу.
В папке docs — файлы спецификации API.
В репозитории нет ни базы данных, ни бекенда, однако сразу после клонирования репозитория вы можете запустить проект и увидеть спецификацию API. По этой спецификации вам предстоит написать API для проекта Foodgram.

# Технические требования и инфраструктура
Проект должен использовать базу данных PostgreSQL.
Код должен находиться в репозитории foodgram-project-react.
В Django-проекте должен быть файл requirements.txt со всеми зависимостями.
Проект нужно запустить в трёх контейнерах (nginx, PostgreSQL и Django) (контейнер frontend используется лишь для подготовки файлов) через docker-compose на вашем сервере в Яндекс.Облаке. Образ с проектом должен быть запушен на Docker Hub.

# Функциональность проекта
Проект доступен по IP или доменному имени.
Все сервисы и страницы доступны для пользователей в соответствии с их правами.
Рецепты на всех страницах сортируются по дате публикации (новые — выше).
Работает фильтрация по тегам, в том числе на странице избранного и на странице рецептов одного автора).
Работает пагинатор (в том числе при фильтрации по тегам).
Исходные данные предзагружены; добавлены тестовые пользователи и рецепты.
## Для авторизованных пользователей:
Доступна главная страница.
Доступна страница другого пользователя.
Доступна страница отдельного рецепта.
Доступна страница «Мои подписки».
1. Можно подписаться и отписаться на странице рецепта.
2. Можно подписаться и отписаться на странице автора.
3. При подписке рецепты автора добавляются на страницу «Мои подписки» и удаляются оттуда при отказе от подписки.
Доступна страница «Избранное».
1. На странице рецепта есть возможность добавить рецепт в список избранного и удалить его оттуда.
2. На любой странице со списком рецептов есть возможность добавить рецепт в список избранного и удалить его оттуда.
Доступна страница «Список покупок».
1. На странице рецепта есть возможность добавить рецепт в список покупок и удалить его оттуда.
2. На любой странице со списком рецептов есть возможность добавить рецепт в список покупок и удалить его оттуда.
3. Есть возможность выгрузить файл (.txt или .pdf) с перечнем и количеством необходимых ингредиентов для рецептов из «Списка покупок».
4. Ингредиенты в выгружаемом списке не повторяются, корректно подсчитывается общее количество для каждого ингредиента.
Доступна страница «Создать рецепт».
1. Есть возможность опубликовать свой рецепт.
2. Есть возможность отредактировать и сохранить изменения в своём рецепте.
3. Есть возможность удалить свой рецепт.
Доступна и работает форма изменения пароля.
Доступна возможность выйти из системы (разлогиниться).
## Для неавторизованных пользователей
Доступна главная страница.
Доступна страница отдельного рецепта.
Доступна страница любого пользователя.
Доступна и работает форма авторизации.
Доступна и работает система восстановления пароля.
Доступна и работает форма регистрации.
## Администратор и админ-зона
Все модели выведены в админ-зону.
Для модели пользователей включена фильтрация по имени и email.
Для модели рецептов включена фильтрация по названию, автору и тегам.
На админ-странице рецепта отображается общее число добавлений этого рецепта в избранное.
Для модели ингредиентов включена фильтрация по названию.
## Инфраструктура
Проект работает с СУБД PostgreSQL.
Проект запущен на сервере в Яндекс.Облаке в трёх контейнерах: nginx, PostgreSQL и Django+Gunicorn. Заготовленный контейнер с фронтендом используется для сборки файлов.
Контейнер с проектом обновляется на Docker Hub.
В nginx настроена раздача статики, запросы с фронтенда переадресуются в контейнер с Gunicorn. Джанго-админка работает напрямую через Gunicorn.
Данные сохраняются в volumes.
## Оформление кода
Код соответствует PEP8.


# Установка и запуск:
## Автоматический запуск:
- На удалённом сервере установить Doker: ```'sudo apt install docker.io'```
- Установите docker-compose: 'https://docs.docker.com/compose/install/'
- Положить в домашнюю дирикторию сервера:
```
    'infra/docker-compose.yaml',
    'infra/nginx.conf',
    'data/',
    'docs/',
    'frontend/'
```
- Выполнить команды:
```
    'docker-compose up -d --build'
    'docker-compose web make run'
```
***Необходим заполненный файл .env в src (смотри ниже)***

Структура файла .env:
```
    ENV=
    DEBUG=
    SECRET_KEY=
    DB_ENGINE=
    DB_NAME=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    DB_HOST=
    DB_PORT=
```
### В кратце, что происходит:
На сервере поднимается три контейнера: postgres, nginx и проект. И frontend, который делает свои дела и падает (в хорошем смылсе). Nginx принимает запросы на :80 порт и переадресует запросы на бекенд (gunicorn) :8000. Здесь же раздаётся статика и фронтенд. Команда **make run** запускает создание миграций, статики, загружает в БД первоначальные данные и создаёт супервользователя.

## Ручной запуск (локально):
- Забираем проект: ```'git clone'```
- Переходим в каталог backend/src/
- Изолируем проект: ```'python -m venv venv && . ./venv/bin/activate'```
- Устанавливаем зависимости: ```'pip install -r requirements.txt'```
- Делаем миграции:
```
    python manage.py makemigrations auth
    python manage.py makemigrations app
    python manage.py migrate
```
- Подтягиваем статику: ```'python manage.py collectstatic'```
- Загружаем данные: 
```
	python manage.py loaddata tag.json
	python manage.py loaddata ingredient.json
```
- Создаём суперпользователя: ```'python manage.py createsuperuser'```
- Запускаем контейнеры (фронт и nginx) из local: ```'docker-compose up -d --build'```
- Запускаемся: ```'python manage.py runserver'```


![example workflow](https://github.com/voitekhovich/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
