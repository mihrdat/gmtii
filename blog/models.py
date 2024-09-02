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
    name = models.CharField(max_length=55)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Video(BaseModel):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="blog/videos")
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
