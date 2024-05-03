# cft_backend

Для накатывания миграций, если файла alembic.ini ещё нет, нужно запустить в темринале команду:

```
alembic init migrations
```

После этого будет создана папка с миграциями и конфиговский файл для alembic

```
from myapp import mymodel
```

- Далее вводим: ```alembic revision --autogenerate -m "comment"```
- Создана миграция
- Дальше вводим ```alembic upgrade heads```
- 