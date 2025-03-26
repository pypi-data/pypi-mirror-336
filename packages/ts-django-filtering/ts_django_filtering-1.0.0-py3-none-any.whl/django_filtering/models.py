from django.db import models


class Requirement(models.Model):
    details = models.CharField(max_length=100)


class Job(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE)


class Person(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
