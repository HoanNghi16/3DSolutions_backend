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

class UserAccountManager(BaseUserManager):
    def create_user(self, profile, email, password = None, **extra_fields):
        if not email:
            raise ValueError('The email cannot be empty')
        email = self.normalize_email(email)
        user = self.model(profile = profile, email = email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user


class UserAccounts(AbstractBaseUser, PermissionsMixin):
    profile = OneToOneField(Users, on_delete=models.CASCADE, primary_key=True, related_name='user_account')
    email = models.EmailField(unique=True)

    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField('auth.Group', related_name='user_accounts')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='user_accounts')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['profile']
    objects = UserAccountManager()

