from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    # auto_now=True last updated post
    # auto_now_add=True when your first made the post
    # default=timezone.now -> passing function, not a value that's why no .now()
    date_posted = models.DateTimeField(default=timezone.now)
    #on_delete = models.CASCADE if User gets deletes, so does the POST
    author = models.ForeignKey(User, on_delete = models.CASCADE)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog-home")
    
    
