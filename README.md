# Foodgram

## Инструкция для локального запуска.

#### Перейдите в директорию infra и выполните команду.
```
docker-compose -f docker-compose-local.yml up -d
```
#### Если контейнер backend не может подключиться к db выполните команды ниже (опционально).
```
docker container ls  # имя контейнера backend infra-backend-1, но лучше проверьте
docker restart <имя>
```
#### Выполните миграции, соберите статику, создайте админа и загрузите данные в базу данных.
```
docker exec -it <имя> python manage.py migrate
docker exec -it <имя> python manage.py collectstatic
docker exec -it <имя> python manage.py createsuperuser
docker exec -it <имя> python manage.py load_tags_json
docker exec -it <имя> python manage.py load_ingredients_json  # 50 первых ингредиентов
docker exec -it <имя> python manage.py load_ingredients_csv  # все игредиенты
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

