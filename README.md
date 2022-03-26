# api_yamdb

## Описание. Проект YaMDb
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). 
Произведения делятся на категории: «Книги», «Фильмы», «Музыка». 
Список категорий (Category) может быть расширен администратором 
(например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или
послушать музыку. 

В каждой категории есть произведения: книги, фильмы 
или музыка. Например, в категории «Книги» могут быть произведения 
«Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — 
песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен жанр (Genre) из списка предустановленных 
(например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать 
только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям 
текстовые отзывы (Review) и ставят произведению оценку в диапазоне 
от одного до десяти (целое число); из пользовательских оценок формируется 
усреднённая оценка произведения — рейтинг (целое число). 
На одно произведение пользователь может оставить только один отзыв.

Документация по api проекта доступна адресу `<servername>/redoc/`  

## Как запустить проект: 
Клонировать проект и перейти в каталог:

```bash
git clone git@github.com:AlxShvalev/infra_sp2.git
cd infra_sp2/infra/
```

Создать файл .env со следующей структурой:

```dotenv
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=db_name
POSTGRES_PASSWORD=db_password
DB_HOST=db
DB_PORT=5432
```

В файле `/infra/nginx/default.conf` в строке `server_name 127.0.0.1;` 
вместо ip-адреса 127.0.0.1 написать ip-адрес или доменное имя используемого 
сервера
 
Запустить docker-compose:

```bash
sudo docker-compose up -d --build
```

Выполнить команды:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic 
```


## Тестовые данные
В проекте есть тестовые данные в файле `/api_yamdb/fixtures.json`

Для загрузки тестовых данных выполните последовательно команды:

```bash
docker-compose exec web python manage.py shell
# выполнить в открывшемся терминале:
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()

docker-compose exec web python manage.py loaddata fixtures.json 
``` 

## Лицензия
GNU GPLv3

## Статус
![workflow](https://github.com/AlxShvalev/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

### Автор
Алексей Швалёв - студент Я.Практикум
