from django.db import models
from django.contrib.auth.models import User


class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link1 = models.URLField(max_length=250, unique=True)
    link2 = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return f'{self.user}: {self.link1} - {self.link2}'
