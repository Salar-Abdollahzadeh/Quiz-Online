from django.db import models


class Author(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)


class Book(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=100)

    authors = models.ManyToManyField('Author')


class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    due_at = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    name = models.CharField(max_length=300)
    cat = models.ForeignKey(to='Category', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}-{self.cat.name}'


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
