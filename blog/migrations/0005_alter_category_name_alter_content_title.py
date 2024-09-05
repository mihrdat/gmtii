# Generated by Django 4.1.2 on 2024-09-05 07:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_content_delete_video"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(max_length=55, unique=True),
        ),
        migrations.AlterField(
            model_name="content",
            name="title",
            field=models.CharField(max_length=255),
        ),
    ]
