from django.db import models
class Floor(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name