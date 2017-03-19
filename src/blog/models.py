from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    category_short = models.CharField(max_length=3, unique=True)

    class Meta:
        ordering = ["category_short"]

    def __str__(self):
        return self.category_name


class Post(models.Model):

    PUBLISHED = "PUB"
    NO_PUBLISHED = "NPB"

    PUBLISH = (
        (PUBLISHED, "Published"),
        (NO_PUBLISHED, "No Published")
    )

    owner = models.ForeignKey(User, related_name="owned_posts")
    title = models.CharField(max_length=100)
    post_intro = models.CharField(max_length=150)
    post_body = models.TextField()
    post_img = models.URLField(null=True, blank=True)
    post_category = models.ManyToManyField(Category)
    post_published = models.CharField(max_length=3, default=PUBLISHED, choices=PUBLISH)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title




