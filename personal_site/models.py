from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100)

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()