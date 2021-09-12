from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#Costume account manager
class MyAccountMenager(BaseUserManager):
    #Izrada usera
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
			email=email,
			username=username,
		)

        user.set_password(password)
        user.save(using=self._db)
        return user

    #Izrada superusera
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

#Dohvacanje filepath-a slike
def get_profile_image_filepath(self):
    return 'profile_images/' + str(self.pk) + 'profilna.png'

#Path za default sliku
def get_default_profile_image():
    return 'profile_images/default.png'

#costume account models sa usernamom umijesto emaila 
class Account(AbstractBaseUser):

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    datum_dolaska = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    zadnji_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountMenager()

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_lable):
        return self.is_admin