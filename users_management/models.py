import uuid
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
import django.contrib.auth
from django.db.models import OneToOneField
from unicodedata import normalize

# Create your models here.

class Users(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    phone =models.CharField(max_length=15)
    date_of_birth = models.DateField()

    def get_name(self):
        return self.name

    def get_phone(self):
        return self.phone

    def get_date_of_birth(self):
        return self.date_of_birth

    def __str__(self):
        return str({ 'name':{self.name}, 'date_of_birth': {self.date_of_birth}, 'phone': {self.phone}})


class UserAccountManager(BaseUserManager):
    def create_user(self, profile, email, password = None, **extra_fields):
        if not email:
            raise ValueError('The email cannot be empty')
        email = self.normalize_email(email)
        user = self.model(profile = profile, email = email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, profile, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(profile, email, password, **extra_fields)

class UserAccounts(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = OneToOneField(Users, on_delete=models.CASCADE, related_name='user_account')
    email = models.EmailField(unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['profile']
    objects = UserAccountManager()

