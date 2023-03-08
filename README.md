# APInews

# Дислеймер
При написании сервиса преследовалась цель сделать его как можно более расширяемым, 
насколько это возможно в рамках выделеных сроков

## Структура проекта

Проект разделен на 2 смысловые части: АПИ и Парсер

Парсер отвечает за сбор данных с сайтов, апишка же отдает спраршенные данные по условиям фильтров

Всего в проекте 2 эндпойнта

Первый:
Сделан строго в соответствии с ТЗ, в качестве параметра принимает кол-во дней и отдает данные
которые были спаршены в промежутке _сегодняшняя дата_ минус количество переданное в параметре.


`/news/metro`

Второй:
Второй эндпойнт, по сути такой же, но дополнительно позваляет применять пагинацию, а так же фильтры к запросу

`/news/metro_extended`

С более подробной спецификацией можно будет ознакомиться на OpenAPI по адресу
localhost:8000/docs после запуска


## Запуск проекта

Для того, чтобы запустить проект, необходимо спулить к себе репозиторий
В корневой папке проекта написать следущие команды в определенном порядке:

`docker compose build`

`docker compose up`

После того, как проект соберется, каждые 10 минут будет запускаться парс сайта

А так же станет доступен сам апи-сервис по адресу localhost:8000

P.S. У меня в compose файле лежат секреты для сервисов, в реальных проектах лучше определять их в файле .env при деплое и уже оттуда подтягивать их в compose файл.
Просто хотелось сделать как можно более простым запуск проекта без создания доп.файлов

