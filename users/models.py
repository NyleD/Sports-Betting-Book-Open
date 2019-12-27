from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from rest_framework import serializers

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user.username} Profile'

    def set_verified(self, val):
        self.verified = val

    def save(self, **kwargs): 
        super().save()
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)



class ProfileSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('id','user','verified', 'photo_url') 

    def get_photo_url(self, profile):
        request = self.context.get('request')
        photo_url = profile.image.url
        return request.build_absolute_uri(photo_url)

# Overriding the parent save functionailty that already exists 
def save(self):
    super().save()

    img = Image.open(self.image.path)

    if img.height > 300 or img.width > 300:
        output_size = (300,300)
        img.thumbnail(output_size)
        img.save(self.image.path)
        self.user.profile.verified = False
        super().save()

