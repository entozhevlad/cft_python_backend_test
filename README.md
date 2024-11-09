# Тестовое задание на курс "Разарботка Backend сервисов на Python"

REST сервис для получения информации о зарплате и дате следующего её повышения по логину и парою на курс "Разработка Backend сервисов на Python
Для накатывания миграций, если файла alembic.ini ещё нет, нужно запустить в темринале команду:

# Инструкция по установке и запуску
Первым делом необходимо клонировать репозиторий:
````
git clone https://gitlab.com/test9421118/cft_backend.git
````
## Запуск из Docker 
Для последующей работы необзходимо установить docker. Скачать его можно на официальном сайте https://www.docker.com/products/docker-desktop

После установик докер, необходимо поднять контейнер

```bash
docker-compose -f docker-compose-ci.yaml up -d 
```
Затем необходимо провести миграции. Выполните команду
```bash
docker exec -it cft_backend bash
````
В открывшемся терминале введите
````
alembic upgrade heads
````
Закройте терминал Docker введя команду
````
exit
````
Проверьте, запущены ли контейнеры через команду 
```
docker ps
```
Если вы видите, что запущено три контейнера то вы можете перейти по адресу для проверки работоспособности сервиса
```
http://localhost:8080/docs
```
- Для создания пользователя, измените данные в теле запроса. Обязательное укажите  зарплату больше 0. 
Создав пользователя 
- Вы сможете авторизоваться нажав на замочек во вкладке Get Current User Salary 
- Для авторизации введите логин и пароль созданного пользователя.

### Тестирование через Postman
Вы можете протестировать работу приложения через Postman, после запуска контйнера.
Для создания пользователя, выполните POST запрос по адресу 
````
http://localhost:8080/user/
````
Тело запроса должно быть следующим
```
{
    "username": "user",
    "first_name": "Mikhail",
    "last_name": "Zubenko",
    "email": "test@gmail.com",
    "password": "76540123",
    "salary_amount": 1000
}
```
Для авторизации пользователя, выполните POST запрос по адресу  http://0.0.0.0:8080/login/token

В Body выберите тип x-www-form-urlencoded и введите следующие данные
```
username: string
password: string
```
В теле запроса вы получите access_token, который действует в течении 30 минут. Время действия можно задать через файл setting или .env

Чтобы получить данные о зарплате, выполните GET запрос по адресу http://0.0.0.0:8080/login/salary
- Скопируйте полученный токен. 
- Затем Выберите вкладку Authorization 
- В ней выберите Auth Type Bearer Token
- Вставьте токен в поле Token и нажмите Send
- В теле ответа будет информация о зарплате следующем повышении пользователя


Когда пользователь создан, вы можете авторизоваться
После этого будет создана папка с миграциями и конфиговский файл для alembic
# Запуск локально
После клонирования репозитория, необходимо создать виртуально окружение и установить зависимости. Вам потребуется установленный язык Python

Первым делом создайте виртуальное окружение
```bash
python -m venv .venv
```
Активируйте его
```bash
.venv\Scripts\activate
```
Теперь установить зависимости из файла requirements.txt
````bash
pip install -r requirements.txt
````
Далее потребуется выполнить ряд действий для запуска локально
- Перейдите в файл main и раскоментируй последние строчки с if __name__ == "__main__"
- Следующим шагом зайдите в файле alembic.ini и в строке sqlalchemy.url =  postgresql://postgres:postgres@db:5432/postgres замените db на localhost
- Затем необходимо создать базу данных. Для этого введите команду
````bash
docker compose -f docker-compose-local.yaml up -d
````
- После этого необходимо создать миграции. Для этого введите команду
````bash
alembic upgrade heads
````
- Запустите файл main.py
- Перейдите по адресу http://localhost:8080/docs

### Тестирование через Pytest

В вашей IDE откройте папку tests и перейдите в файле test_handlers. Запустить его при помощи Pycharm


#### Для того чтобы во время тестов нормально генерировались миграции нужно"

- сначала попробовать запустить тесты обычным образом. с первого раза всё должно упасть
- если после падения в папке tests создались файлы alembic, то нужно прописать туда данные подключения к базе данных, а именно в строке sqlalchemy.url = postgresql://postgres:postgres@localhost:5432/postgres
- В папке migrations пропишите 
- ``` 
  from db.models import Base
  ```
- Также в target_metadadata установите параметр с None на Base.metadata
- 