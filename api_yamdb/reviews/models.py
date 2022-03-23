from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator
from users.models import User


class Title(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    year = models.PositiveIntegerField(
        verbose_name='Год создания',
        validators=(year_validator,)
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        'Category',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        'Genre',
        related_name='titles',
    )

    def genre_names(self):
        return [genre for genre in
                Title.objects.values_list('genre__name',
                                          flat=True).filter(pk=self.pk)]

    genre_names.short_description = 'Жанры'

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField('Адрес категории', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1, 'Оценка не может быть меньше 1'),
            MaxValueValidator(10, 'Оценка не может быть больше 10')
        ]
    )
    title = models.ForeignKey(
        'Title',
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title', ],
                name='unique review',
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date', )

    def __str__(self):
        return self.text[:60]


class Comment(models.Model):
    text = models.TextField('comment text', blank=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True,
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
