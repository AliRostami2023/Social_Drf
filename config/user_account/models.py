from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from datetime import datetime, timedelta



class User(AbstractBaseUser):
    phone_number = models.CharField(_('phone number'), max_length=11, unique=True, blank=True)
    username = models.CharField(max_length=120, unique=True, verbose_name=_('username'))
    date_join = models.DateTimeField(auto_now_add=True, verbose_name=_('date join'))
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()


    def __str__(self) -> str:
        return f'{self.phone_number} - {self.username}'

    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    


class OtpCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otpuser', verbose_name=_('user'))
    code = models.PositiveIntegerField(_('code'))
    expired_date = models.DateTimeField(_('expired date'))


    def __str__(self) -> str:
        return f"{self.user.username} +' '+ {self.code}"
    
    
    @property
    def expired_date_over(self):
        return datetime.now() > self.expired_date
    

    @property
    def delete_otp(self):
        if self.expired_date_over():
            self.delete()
            return True
        return False



class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_user', verbose_name=_('user'))
    full_name = models.CharField(max_length=300, verbose_name=_('full name'))
    email = models.EmailField(max_length=300, unique=True, null=True, blank=True, verbose_name=_('email'))
    avatar = models.ImageField(upload_to='avatar_user/%y/%m/%d', null=True, blank=True, verbose_name=_('avatar user'))
    about_me = models.TextField(max_length=1000, verbose_name=_('about me'), null=True, blank=True)

    Gender = (
        ('male', 'male'), ('female', 'female')
    )

    gender = models.CharField(max_length=6, choices=Gender, verbose_name=_('gender'))
    birthday = models.DateField(null=True, blank=True, verbose_name=_('birthday'))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f"{self.full_name} - {self.user.username}"


    class Meta:
        ordering = ('-created', '-updated',)
    