from rest_framework import serializers

from .models import Author, Category, Comment, Post, Tag


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['name', "email", "body", 'created_on']
