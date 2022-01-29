from django.db import models
from tkinter import CASCADE
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin


# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self,email,firstname,secondname,phone,password=None):
        if not email:
            raise ValueError('You must have an email')

        user = self.model(
            email = self.normalize_email(email),
            firstname = firstname,
            secondname = secondname,
            phone = phone,
            is_active = 1,
        )

        user.set_password(password)
        user.save(using=self._db)
        self.phone = phone
        return user

    def create_superuser(self,email,password=None):
        superuser = self.model(
        email = self.normalize_email(email),
            is_active =1,
            is_superuser =1,
            is_staff = 1,
            
        )
        superuser.set_password(password)
        superuser.save(using=self._db)
        return superuser

class Account(AbstractBaseUser,PermissionsMixin):
    firstname = models.CharField(max_length=50)
    secondname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50,unique=True)
    phone = models.BigIntegerField(unique=True,default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    create_superuser = models.CharField(max_length=100,default=True)


    USERNAME_FIELD='email'
    REQUIRED_FIELD = ['firstname','email', 'phone', 'password']

    objects = AccountManager()

class Address(models.Model):
    user = models.ForeignKey(Account,default=True,on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50,blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.IntegerField()
    address = models.CharField(max_length=200)
    phone = models.BigIntegerField()
    is_active = models.IntegerField(default=False)
 