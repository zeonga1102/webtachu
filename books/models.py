from django.db import models

# Create your models here.
class BookModel(models.Model):

    class Meta:
        db_table = "books"

    cover = models.TextField()
    title = models.CharField(max_length=50)
    genre = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    publisher = models.CharField(max_length=20)
    story = models.TextField()
    star = models.FloatField(default=0.0)

    def __str__(self):
        return f'[{self.genre}] {self.title}'

