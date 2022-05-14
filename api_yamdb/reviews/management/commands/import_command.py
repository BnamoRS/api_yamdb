from unicodedata import category
from django.core.management.base import BaseCommand
import csv
import sqlite3

from reviews.models import Comment, Review, User, Genre, Title, Category


models_and_files = {
    'review.csv': Review,
    'comment.csv': Comment
}


class Command(BaseCommand):
    help = "Импортирует данные из csv файлов в базу данных"

    def handle(self, **kwargs):
        for file_name in ['users.csv', 'genre.csv', 'category.csv', 'titles.csv', 'review.csv', 'comments.csv', 'genre_title.csv']:
            with open('static/data/' + file_name, 'r', newline='', encoding='UTF-8') as file:
                reader = csv.reader(file, delimiter=",")
                start = True
                for row in reader:
                    print(row)
                    if start:
                        columns = row
                        start = False
                    elif file_name == 'users.csv':
                        User.objects.get_or_create(
                            id=row[columns.index('id')],
                            username=row[columns.index('username')],
                            email=row[columns.index('email')],
                            role=row[columns.index('role')],
                            bio=row[columns.index('bio')],
                            first_name=row[columns.index('first_name')],
                            last_name=row[columns.index('last_name')],
                        )
                    elif file_name == 'genre.csv':
                        Genre.objects.get_or_create(
                            id=row[columns.index('id')],
                            name=row[columns.index('name')],
                            slug=row[columns.index('slug')],
                        )
                    elif file_name == 'category.csv':
                        Category.objects.get_or_create(
                            id=row[columns.index('id')],
                            name=row[columns.index('name')],
                            slug=row[columns.index('slug')],
                        )
                    elif file_name == 'titles.csv':
                        category_id = row[columns.index('category')]
                        Title.objects.get_or_create(
                            id=row[columns.index('id')],
                            name=row[columns.index('name')],
                            year=row[columns.index('year')],
                            category=Category.objects.get(pk=category_id),
                        )
                    elif file_name == 'review.csv':
                        title = row[columns.index('title_id')]
                        author = row[columns.index('author')]
                        Review.objects.get_or_create(
                            id=row[columns.index('id')],
                            text=row[columns.index('text')],
                            score=row[columns.index('score')],
                            pub_date=row[columns.index('pub_date')],
                            title=Title.objects.get(pk=title),
                            author=User.objects.get(pk=author),
                        )
                    elif file_name == 'comments.csv':
                        review = row[columns.index('review_id')]
                        author = row[columns.index('author')]
                        Comment.objects.get_or_create(
                            id=row[columns.index('id')],
                            text=row[columns.index('text')],
                            pub_date=row[columns.index('pub_date')],
                            review=Review.objects.get(pk=review),
                            author=User.objects.get(pk=author),
                        )
                    elif file_name == 'title.csv':
                        review = row[columns.index('review_id')]
                        author = row[columns.index('author')]
                        Comment.objects.get_or_create(
                            id=row[columns.index('id')],
                            text=row[columns.index('text')],
                            pub_date=row[columns.index('pub_date')],
                            review=Review.objects.get(pk=review),
                            author=User.objects.get(pk=author),
                        )
                    elif file_name == 'genre_title.csv':
                        title_id = row[columns.index('title_id')]
                        genre_id = row[columns.index('genre_id')]
                        title = Title.objects.get(pk=title_id)
                        title.genre.add(Genre.objects.get(pk=genre_id)) 
                        title.save()