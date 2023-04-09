from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Snippet(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.TextField(max_length=5000)
    code_snippet = models.TextField(max_length=5000)
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.question
