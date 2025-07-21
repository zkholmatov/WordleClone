from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    guessed_letters = models.JSONField(default=list, blank=True, null=True)
    score = models.PositiveIntegerField(default=0, blank=True, null=True)
    winstreak = models.PositiveIntegerField(default=0, blank=True, null=True)
    rewarded = models.BooleanField(default=False)

    class Meta:
        ordering = ['-score']


class Answer(models.Model):
    word = models.CharField(max_length=5, default='')

    def __str__(self):
        return self.word
    

class Guess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=5)
    attempt_number = models.PositiveIntegerField(default=0)
    result = models.JSONField(default=list)