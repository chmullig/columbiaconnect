from django.db import models
from django.contrib.auth.models import Group, User

class UserManager(models.Manager):
    def get_query(self):
        return super(UserManager, self).get_query_set().distinct()

class Student(models.Model):
    user = models.OneToOneField(User)
    classyear = models.CharField(max_length=10, blank=True)
    profile = models.TextField(blank=True)

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


    class Meta:
        verbose_name_plural = "Categories"


class Connex(models.Model):
    name = models.CharField(max_length=100)
    #group = models.OneToOneField(Group)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, blank=True)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Connexes"


#pictures of groups
#user pictures


#posts/announcements
#events?
#users in groups