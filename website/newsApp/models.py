from django.db import models

# Create your models here.
class article(models.Model) :
    Title = models.CharField(max_length=200)
    URL = models.CharField(max_length=10000)
    Paragraph = models.TextField()
    Image_URL = models.CharField(max_length=10000)
    Date = models.CharField(max_length=200)
    views = models.IntegerField(default=0)
    def __str__(self):
        return self.Title
