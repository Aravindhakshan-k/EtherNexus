# Generated by Django 4.1.5 on 2023-01-27 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_app1', '0003_rename_post_contentmodel_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contentmodel',
            name='author',
        ),
        migrations.CreateModel(
            name='WebpageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('url', models.URLField()),
                ('background_img', models.ImageField(upload_to='')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_app1.usermodel')),
            ],
        ),
        migrations.AddField(
            model_name='contentmodel',
            name='website',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='test_app1.webpagemodel'),
        ),
    ]
