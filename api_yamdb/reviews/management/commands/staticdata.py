import django.db.utils
import pandas as pd
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

category = pd.read_csv('static/data/category.csv')
titles = pd.read_csv('static/data/titles.csv')
genre = pd.read_csv('static/data/genre.csv')
genre_title = pd.read_csv('static/data/genre_title.csv')
users = pd.read_csv('static/data/users.csv')
review = pd.read_csv('static/data/review.csv')
comment = pd.read_csv('static/data/comments.csv')


def category_create(category):
    list_category = []
    for i in range(len(category)):
        list_category.append(
            Category(
                id=category['id'][i],
                name=category['name'][i],
                slug=category['slug'][i]
            )
        )
    try:
        Category.objects.bulk_create(list_category)
    except django.db.utils.IntegrityError as e:
        print(f'{e} Тестовая база уже была загружена. '
              f'Данная команда выполняется на чистую базу')


def genre_create(titles):
    list_title = []
    for i in range(len(titles)):
        list_title.append(
            Title(
                id=titles['id'][i],
                name=titles['name'][i],
                year=titles['year'][i],
                category=Category.objects.get(pk=titles['category'][i]),
            )
        )
    try:
        Title.objects.bulk_create(list_title)
    except django.db.utils.IntegrityError as e:
        print(f'{e} Тестовая база уже была загружена. '
              f'Данная команда выполняется на чистую базу')


def titles_create(genre):
    list_genre = []
    for i in range(len(genre)):
        list_genre.append(
            Genre(
                id=genre['id'][i],
                name=genre['name'][i],
                slug=genre['slug'][i],
            )
        )
    try:
        Genre.objects.bulk_create(list_genre)
    except django.db.utils.IntegrityError as e:
        print(f'{e} Тестовая база уже была загружена. '
              f'Данная команда выполняется на чистую базу')


def users_create(users):
    list_users = []
    for i in range(len(users)):
        list_users.append(
            User(
                id=users['id'][i],
                username=users['username'][i],
                email=users['email'][i],
                role=users['role'][i],
                bio=users['bio'][i],
                first_name=users['first_name'][i],
                last_name=users['last_name'][i],
                confirmation_code=[i],
            )
        )
    try:
        User.objects.bulk_create(list_users)
    except django.db.utils.IntegrityError as e:
        print(f'{e} Тестовая база уже была загружена. '
              f'Данная команда выполняется на чистую базу')


def review_create(review):
    list_review = []
    for i in range(len(review)):
        list_review.append(
            Review(
                id=review['id'][i],
                title=Title.objects.get(pk=review['title_id'][i]),
                text=review['text'][i],
                author=User.objects.get(pk=review['author'][i]),
                score=review['score'][i],
                pub_date=review['pub_date'][i],
            )
        )
    try:
        Review.objects.bulk_create(list_review)
    except django.db.utils.IntegrityError as e:
        print(f'{e} Тестовая база уже была загружена. '
              f'Данная команда выполняется на чистую базу')


def comment_create(comment):
    list_comment = []
    for i in range(len(comment)):
        list_comment.append(
            Comment(
                id=comment['id'][i],
                review=Review.objects.get(pk=comment['review_id'][i]),
                text=comment['text'][i],
                pub_date=comment['pub_date'][i],
                author=User.objects.get(pk=comment['author'][i]),
            )
        )
    try:
        Comment.objects.bulk_create(list_comment)
    except django.db.utils.IntegrityError:
        print('Тестовая база уже была загружена. '
              'Данная команда выполняется на чистую базу')


trigger = [
    category_create,
    genre_create,
    titles_create,
    users_create,
    review_create,
    comment_create,
]


class Command(BaseCommand):
    help = 'import data to sqlite3'

    def handle(self, *args, **options):
        for i in range(len(trigger)):
            trigger[i]
