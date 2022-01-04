from autoslug.fields import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.urls.base import reverse
from django.utils.translation import ugettext_lazy as _

User = get_user_model()
# Create your models here.


class Book(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    sample = models.FileField(upload_to='books/sample')
    published = models.BooleanField(default=False)
    downloads = models.IntegerField(default=0)
    cover = models.ImageField(upload_to='books/covers')
    slug = AutoSlugField(_('slug'), populate_from='title',
                         unique=True, primary_key=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-view", kwargs={"pk": self.pk, 'slug': self.slug})

    def get_sample_download_link(self):
        return reverse("sample-download", kwargs={"pk": self.pk, 'slug': self.slug})


class BookUser(models.Model):
    email = models.EmailField(unique=True)
