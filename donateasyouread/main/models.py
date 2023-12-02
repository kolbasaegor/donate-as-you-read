from django.db import models
from django.urls import reverse


class User(models.Model):
    name = models.CharField(max_length=100, blank=False)
    username = models.CharField(max_length=64, db_index=True, blank=False)
    hashed_password = models.CharField(max_length=255)
    time_create = models.DateTimeField(auto_now_add=True)
    eth_address= models.CharField(max_length=100, blank=False)

    def get_absolute_url(self):
        return reverse('user', kwargs={'username': self.username})
    
    def __str__(self):
        return self.username


class Article(models.Model):
    title = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(max_length=255, unique=True)
    time_create = models.DateTimeField(auto_now_add=True)
    mins_to_read = models.IntegerField()
    content = models.TextField(blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('article', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-time_create']

