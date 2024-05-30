from django.db import models

# Create your models here.


class User(models.Model):
    vk_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    avatar = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Memory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memories")
    latitude = models.FloatField()
    longitude = models.FloatField()
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

