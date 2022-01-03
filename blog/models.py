from autoslug.fields import AutoSlugField
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import Adjust, ResizeToFill
from PIL.Image import Image

User = get_user_model()


class Service(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'


class Category(models.Model):
    title = models.CharField(max_length=255, blank=False)
    slug = AutoSlugField(populate_from='title',
                         unique=False, primary_key=False)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:category-view', kwargs={'pk': self.pk, 'title': self.slug})


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='blog/authors', blank=True, null=True)
    facebook_page = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.user.first_name

    def first_name(self):
        return self.user.first_name

    def save(self, *args, **kwargs):
        if not self.name and self.user:
            self.name = self.user.get_full_name()
        super().save(*args, **kwargs)


class Tag(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:tag-view', kwargs={'pk': self.pk, 'name': self.title})


class Post(models.Model):
    author = models.ForeignKey(
        Author, blank=True, null=True, on_delete=models.SET_NULL, related_name='posts')
    title = models.CharField(max_length=255, blank=False, null=False)
    slug = AutoSlugField(_('slug'), populate_from='title',
                         unique=True, primary_key=False)
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.SET_NULL, related_name='posts')
    content = RichTextUploadingField(_('content'), blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    published_date = models.DateField(
        auto_now_add=False, blank=True, null=True)
    tags = models.ManyToManyField(
        Tag, blank=True, related_name="posts")
    thumbnail = models.ImageField(
        upload_to='blog', blank=True, null=True, default='blog/default.jpg')
    image_wide = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
                                 ResizeToFill(400, 750)], image_field='thumbnail',
                                format='JPEG', options={'quality': 90})
    image_square = ImageSpecField([Adjust(contrast=1.2, sharpness=1.1),
                                   ResizeToFill(220, 340)], image_field='thumbnail',
                                  format='JPEG', options={'quality': 90})
    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name = "blog"
        ordering = ['-created_on', '-published_date']
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog-detail', kwargs={'pk': self.pk, 'title': self.slug})

    def save(self, *args, **kwargs):
        if self.published and not self.published_date:
            self.published_date = timezone.now()
        if not self.published and self.published_date is not None:
            self.published_date = None
        if not self.summary and self.content:
            text = strip_tags(self.content)
            if len(text) > 200:
                text = '%s ...' % text[:150]
            self.summary = text
        super().save(*args, **kwargs)


class Comment(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=255, blank=False, null=False)
    body = models.TextField(blank=False, null=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=False, blank=False, related_name='comments')
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["approved", "-created_on"]
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.name


class SearchTerms(models.Model):
    term = models.CharField(max_length=255, blank=False, null=False)
    slug = AutoSlugField(_('slug'), populate_from='term')

    def __str__(self):
        return self.term[:20]

    def slug_term(self):
        slug = self.term.replace(" ", "+")
        return slug

    def get_absolute_url(self):
        return "/blog/search/?q=%s" % self.term


class UniqueUser(models.Model):
    session_key = models.CharField(max_length=250)
    ip = models.GenericIPAddressField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
