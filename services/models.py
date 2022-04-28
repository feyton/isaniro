from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return super().__str__()
