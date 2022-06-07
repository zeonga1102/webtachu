from django.db import models
from books.models import BookModel
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserModel(AbstractUser):

    class Meta:
        db_table = "users"

    favorite = models.ManyToManyField(BookModel)


class ReviewModel(models.Model):

    class Meta:
        db_table = "reviews"

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    star = models.IntegerField()
    desc = models.TextField()
    date = models.DateTimeField(auto_now_add=True)