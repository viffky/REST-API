Проект включает в себя docker-compose.yml, который позволяет запустить приложение и базу данных PostgreSQL в контейнерах.

Шаги для запуска:
Убедитесь, что у вас установлен Docker и Docker Compose.

Перейдите в директорию проекта:
```
cd C:\Users\Sladkaya\Desktop\rest_api\backend_task
```
Запустите Docker Compose:
```
docker-compose up --build
```
После успешного запуска вы сможете получить доступ к API по адресу: http://localhost:8000

Документация OpenAPI будет доступна по адресу: http://localhost:8000/docs

не забудьте про .env и ссылкой подключения для postgres
