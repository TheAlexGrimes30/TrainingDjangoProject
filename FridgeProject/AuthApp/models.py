from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import bcrypt

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('role', CustomUser.Role.STAFF)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, email, password, **extra_fields)

    def create_admin(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('role', CustomUser.Role.ADMIN)
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser):

    class Role(models.TextChoices):
        USER = 'user', _('User')
        STAFF = 'staff', _('Staff')
        ADMIN = 'admin', _('Admin')

    username = models.CharField(max_length=256, unique=True)
    email = models.EmailField(unique=True)
    password = models.TextField()
    role = models.CharField(
        max_length=16,
        choices=Role.choices,
        default=Role.USER
    )
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def set_password(self, raw_password):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))
    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"
        indexes = [
            models.Index(["date_joined"], name="date_joined_index"),
        ]

