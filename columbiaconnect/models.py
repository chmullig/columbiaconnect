from django.db import models
from django.contrib.auth.models import Group, User
from django.utils.text import slugify

class UserManager(models.Manager):
    def get_query(self):
        return super(UserManager, self).get_query_set().distinct()

class Student(models.Model):
    user = models.OneToOneField(User)
    classyear = models.CharField(max_length=10, blank=True)
    profile = models.TextField(blank=True)
    def _slugify(self):
        return slugify(email)
    url = property(_slugify)


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
    def _slugify(self):
        return slugify(name)
    url = property(_slugify)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Connexes"

class Message(models.Model):
    sender = models.ForeignKey(User)
    connex = models.ForeignKey(Connex)
    subject = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    body = models.TextField()
    def __str__(self):
        return "%s to %s @ %s" % (self.sender, self.connex, self.date)

    class Meta:
        verbose_name_plural = "Messages"

#pictures of groups
#user pictures


#posts/announcements
#events?
#users in groups