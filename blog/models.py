from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Publisher(BaseModel):
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="publisher"
    )


class Category(BaseModel):
    name = models.CharField(max_length=55, unique=True)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Content(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to="blog/videos")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name="contents")

    def __str__(self):
        return self.title
