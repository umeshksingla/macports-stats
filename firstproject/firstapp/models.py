import uuid
from django.contrib.postgres.fields import JSONField
from django.db import models

MAX_LENGTH = 255

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class Submission(models.Model):
    data = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class User(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(
        unique=True,
        max_length=MAX_LENGTH,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']


class Port(models.Model):
    name = models.CharField(
        unique=True,
        max_length=MAX_LENGTH,
    )
    path = models.CharField(max_length=255)
    version = models.CharField(max_length=MAX_LENGTH)
    description = models.TextField()
    licenses = models.CharField(max_length=MAX_LENGTH)
    variants = models.CharField(max_length=MAX_LENGTH)
    maintainers = models.CharField(max_length=MAX_LENGTH)
    platforms = models.CharField(max_length=MAX_LENGTH)
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']


class InstalledPort(models.Model):
    port_id = models.ForeignKey(
        Port,
        on_delete=models.CASCADE
    )
    version = models.CharField(max_length=MAX_LENGTH)
    variants = models.CharField(max_length=MAX_LENGTH)
    requested = models.IntegerField(default=0)
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OsStatistic(models.Model):
    macports_version = models.CharField(max_length=MAX_LENGTH)
    osx_version = models.CharField(max_length=MAX_LENGTH)
    os_arch = models.CharField(max_length=MAX_LENGTH)
    os_platform = models.CharField(max_length=MAX_LENGTH)
    build_arch = models.CharField(max_length=MAX_LENGTH)
    xcode_version = models.CharField(max_length=MAX_LENGTH)
    gcc_version = models.CharField(max_length=MAX_LENGTH)
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
