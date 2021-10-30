from django.db import models


class Subscriber(models.Model):
    name = models.CharField(max_length=100,)
    email = models.EmailField()
    active = models.BooleanField(default=True, null=False)
    date_subscribed = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-name']
        verbose_name = "Uwiyandikishije"
        verbose_name_plural = "Abiyandikishije"

    def __str__(self):
        return self.name
