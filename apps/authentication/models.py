from django.db import models
# from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Models of users"""
    email = models.EmailField('email address', unique=True, error_messages={
        'unique': 'A user with that email already exists.'
    })
    is_client = models.BooleanField(
        'client status',
        default=False,
        help_text=('Help easily distinguish users and perform queries.')
    )
    is_verified = models.BooleanField(default=False, help_text='Set to true when the user verified its email address.')
    createad_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username
    
    def get_short_name(self):
        return self.username
    
    # def make_random_password(self, length=10,
    #                         allowed_chars='abcdefghjkmnpqrstuvwxyz'
    #                                       'ABCDEFGHJKLMNPQRSTUVWXYZ'
    #                                       '23456789'):
    #     """
    #     Generate a random password with the given length and given
    #     allowed_chars. The default value of allowed_chars does not have "I" or
    #     "O" or letters and digits that look similar -- just to avoid confusion.
    #     """
    #     return get_random_string(length, allowed_chars)
