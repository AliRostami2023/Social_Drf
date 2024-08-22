from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, full_name, email, username, password=None):
        """
        Creates and saves a User with the given email, full_name
         , username and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        
        if not full_name:
            raise ValueError('Users must have an full name')
        
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, full_name=None, password=None):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            full_name=full_name
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    