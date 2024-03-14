from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser , PermissionsMixin
from django.db.models.signals import post_save
from PIL import Image
from rest_framework.permissions import IsAuthenticated
from django.template.defaultfilters import slugify


import uuid
class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
       
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        email = email.lower()
        
        user = self.model(
            email=email,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password=None , **kwargs):
       
        user = self.create_user(
            email,
            password=password,
            **kwargs 
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user


class UserAccount(AbstractBaseUser , PermissionsMixin):
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    artistname= models.CharField(max_length=255 , unique=True , blank=True , null=True)
    email = models.EmailField( unique=True , max_length=255)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(
        upload_to='images/',
        null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    background = models.ImageField(
        upload_to='images/',
        null=True)
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name' ]
    
    def get_image(self):
        if self.profile_pic:
            return 'http://127.0.0.1:8000/' + self.profile_pic.url
        return ''
    
    def get_background(self):
         if self.background:
            return 'http://127.0.0.1:8000/' + self.background.url
         return ''
    
   
    def __str__(self):
        return self.email


class Profile(models.Model):
    
    account = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='acc', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/' )
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    track = models.FileField(upload_to='music/')
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(blank=True , null=True)
    key = models.SlugField(null=True , blank=True)
    ky = models.SlugField(null=True, blank=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.unique_id}'
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000/' + self.image.url
        return ''
    
    def get_absolute_url(self):
        return f'/{self.slug}/'
    
   
    
    def tracks(self):
        if self.track:
            return 'http://127.0.0.1:8000/' + self.track.url
        return ''
        
    def comments(self):
        ''' Get all comments '''
        return Comment.objects.filter(post__id=self.pk)
 
 
class Comment(models.Model):
    content = models.CharField(max_length=200, blank=True)
    post = models.ForeignKey(Profile ,on_delete=models.CASCADE, related_name='post', null=True , blank=True)
    author = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='author')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) 
    slug = models.SlugField()
    
     
  
    
    def __str__(self):
        return f"Comment on {self.post}"


   
    def __str__(self):
        return f"{self.content} on {self.post} by {self.author.artistname}"
     
    def get_absolute_url(self):
        return f'/{self.post.slug}/{self.slug}/'
  
    
    def get_absolute_url(self):
        return f'/{self.slug}/'

