from django.db import models


class Parent(models.Model):
    name = models.CharField(max_length=50)


class Related1(models.Model):
    r1parent = models.ForeignKey(Parent)
    name = models.CharField(max_length=50)


class Related2(models.Model):
    r2parent = models.ForeignKey(Parent)
    name = models.CharField(max_length=50)
