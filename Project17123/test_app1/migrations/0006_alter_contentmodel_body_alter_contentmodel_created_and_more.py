# Generated by Django 4.1.5 on 2023-01-30 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app1', '0005_alter_contentmodel_body_alter_contentmodel_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentmodel',
            name='body',
            field=models.TextField(max_length=6000, unique=True),
        ),
        migrations.AlterField(
            model_name='contentmodel',
            name='created',
            field=models.DateField(auto_now=True, unique=True),
        ),
        migrations.AlterField(
            model_name='contentmodel',
            name='image',
            field=models.ImageField(unique=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='contentmodel',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='contentmodel',
            name='title',
            field=models.CharField(default='Title', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='contentmodel',
            name='updated',
            field=models.DateField(auto_now_add=True, unique=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='password',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='user_id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='webpagemodel',
            name='background_img',
            field=models.ImageField(unique=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='webpagemodel',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='webpagemodel',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]
