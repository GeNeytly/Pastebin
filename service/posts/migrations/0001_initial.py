# Generated by Django 4.2.6 on 2023-12-03 17:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title of the post')),
                ('text', models.TextField(verbose_name='text of the post')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='post creation date')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='author of the post')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='name of the tag')),
                ('description', models.TextField(verbose_name='description of tag')),
                ('slug', models.SlugField(max_length=20, unique=True, verbose_name='unique slug of tag')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expire_time', models.DateTimeField(verbose_name='when the post will no longer be available')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='posts.post', verbose_name='post that the author is sharing')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='posts.tag', verbose_name='related tags of the post'),
        ),
    ]
