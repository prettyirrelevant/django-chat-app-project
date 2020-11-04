from hashlib import md5
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def _create_user(self, username, email, password):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("Email Address must be provided")
        if not username:
            raise ValueError("Username must be provided")

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None):
        return self._create_user(username, email, password)

    def create_superuser(self, username, email, password=None):
        user = self.create_user(email, username, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    username = models.CharField(unique=True, max_length=30)
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )
    is_admin = models.BooleanField(
        "admin status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    date_joined = models.DateTimeField("date joined", default=timezone.now)

    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"
    objects = MyUserManager()

    def __str__(self):
        return self.email

    @property
    def avatar(self):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s=64".format(digest)

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
