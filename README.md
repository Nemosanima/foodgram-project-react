# Foodgram
![example workflow](https://github.com/nemosanima/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

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
#### Создайте папку infra
```
cd ~
mkdir infra
```
#### Перенести файлы docker-compose.yml, nginx.conf и .env с вашего ПК на сервер.
Не забудьте добавить ip сервера в CSRF_TRUSTED_ORIGINS и ALLOWED_HOSTS
```
scp docker-compose.yml username@server_ip:/home/username/infra/
scp nginx.conf username@server_ip:/home/username/infra/
scp .env username@server_ip:/home/username/infra/
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
sever_ip
```
#### Докементация по API
```
server_ip/api/docs/
```
#### Админка
```
server_ip/admin/
```
