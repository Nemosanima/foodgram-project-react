# Foodgram
![example workflow](https://github.com/nemosanima/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

## Описание

Foodgram - это сервис, который позволяет пользователям публиковать рецепты, подписываться на других пользователей, добавлять любимые рецепты в список "Избранное" и скачивать сводный список продуктов перед походом в магазин для приготовления выбранных блюд. Foodgram предоставляет удобную платформу для обмена рецептами и вдохновения в кулинарной области. Это место, где пользователи могут делиться своими любимыми блюдами, находить новые идеи для готовки и наслаждаться кулинарным опытом в сообществе единомышленников.

![Index](https://github.com/Nemosanima/foodgram-project-react/blob/master/images/index.png)

## Основной стек

- #### Django
- #### DRF
- #### Postgres
- #### Nginx
- #### Docker Compose
- #### React

## Инструкция для локального запуска

#### Перейдите в директорию infra и выполните команду
```
docker-compose -f docker-compose-local.yml up -d
```
#### Если контейнер backend не может подключиться к db выполните команды ниже (опционально)
```
docker container ls  # имя контейнера backend infra-backend-1, но лучше проверьте
docker restart <имя>
```
#### Выполните миграции, соберите статику, создайте админа и загрузите данные в базу данных
```
docker exec -it <имя> python manage.py migrate
docker exec -it <имя> python manage.py collectstatic
docker exec -it <имя> python manage.py createsuperuser
docker exec -it <имя> python manage.py load_tags_json
docker exec -it <имя> python manage.py load_ingredients_json  # 50 рандомных ингредиентов
docker exec -it <имя> python manage.py load_ingredients_csv  # около 2х тысяч ингредиентов
```
#### Foodgram
```
localhost
```
#### Докементация по API
```
localhost/api/docs/
```
#### Админка
```
localhost/admin/
```

## Инструкция для запуска на удаленном сервере

#### Secrets для CI/CD
```
# В Settings - Secrets and variables - Actions 
добавьте secrets c вашими данными
# Это необходимо для работы CI/CD, DockerHub, GitHub
DOCKER_USERNAME
DOCKER_USERNAME
HOST
USER
SSH_KEY
PASSPHRASE
DB_ENGINE
DB_NAME
POSTGRES_USER
POSTGRES_PASSWORD
DB_HOST
DB_PORT
TELEGRAM_TO
TELEGRAM_TOKEN
```
#### Покдлючитесь к серверу
```
ssh username@server_ip
```
#### Следующая команда совершает 3 действия:
- Обновляет список доступных пакетов и их версии из основных репозиториев. Так система узнает о доступных обновлениях.
- Устанавливает обновления для всех установленных пакетов на вашей системе.
- Устанавливает пакет curl на вашей системе.
```
sudo apt update && sudo apt upgrade -y && sudo apt install curl -y
```
#### Загрузите и запустите скрипт установки Docker, который в свою очередь установит Docker на вашу систему
```
sudo curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo rm get-docker.sh
```
#### Загрузите файл Docker Compose
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
#### Эта команда устанавливает исполняемый флаг для файла docker-compose, что позволяет использовать docker-compose команду из любого места в системе.
```
sudo chmod +x /usr/local/bin/docker-compose
```
#### Это команда позволит вам использовать Docker без необходимости вручную запускать сервис каждый раз после перезагрузки системы.
```
sudo systemctl start docker.service && sudo systemctl enable docker.service
```
#### Создайте папку infra и docs
```
cd ~
mkdir infra
mkdir docs
```
#### Перенести файлы docker-compose.yml, nginx.conf и .env, openapi-chema.yml и redoc.html с вашего ПК на сервер.
Не забудьте добавить ip сервера в server_name
```
scp docker-compose.yml username@server_ip:/home/username/infra/
scp nginx.conf username@server_ip:/home/username/infra/
scp .env username@server_ip:/home/username/infra/
scp openapi-chema.yml username@server_ip:/home/username/docs/
scp redoc.html username@server_ip:/home/username/docs/
```
Пример файла .env
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
#### На своем ПК соберите образы для backend и frontend, запуште их на DockerHub и изменить docker-compose под свои images.
Не забудьте добавить ip сервера в CSRF_TRUSTED_ORIGINS и ALLOWED_HOSTS
```
docker login
docker build -t username/название_образа:latest .
docker push username/название_образа:latest
```
#### На удаленном сервере перейдите в папку infra и выполните команду
```
sudo docker-compose up -d --build
```
####  Выполните миграции, соберите статику, создайте админа и загрузите данные в базу данных

```
sudo docker container ls -a  # посмотрите название контейнера backend
sudo docker exec -it <имя> python manage.py migrate
sudo docker exec -it <имя> python manage.py collectstatic
sudo docker-compose exec <имя> python manage.py createsuperuser
sudo docker exec -it <имя> python manage.py load_tags_json
sudo docker exec -it <имя> python manage.py load_ingredients_json  # 50 рандомных ингредиентов
sudo docker exec -it <имя> python manage.py load_ingredients_csv  # около 2х тысяч ингредиентов
```
#### Foodgram
```
server_ip
```
#### Докементация по API
```
server_ip/api/docs/
```
#### Админка
```
server_ip/admin/
```