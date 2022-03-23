from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    STATUSES = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN)
    )

    role = models.CharField(max_length=9, choices=STATUSES, default=USER)
    email = models.EmailField(
        help_text='email address',
        unique=True,
    )
    bio = models.TextField(
        max_length=300,
        blank=True
    )
    confirmation_code = models.SlugField(
        max_length=10,
        blank=True,
    )

    def is_moderator(self):
        return self.role == self.MODERATOR

    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser
