from django.db import models


class Paste(models.Model):
    title = models.CharField(max_length=30)
    text = models.TextField()
    url = models.URLField()
