from django.db import models

# Create your models here.
class UserModel(models.Model):
    user_id = models.AutoField(
        primary_key=True,
        unique=True,
        null=False,
        blank=False
    )
    name = models.CharField(
        max_length=50,
        blank=False,
        unique=True
    )
    email = models.EmailField(
        max_length=50,
        blank=False,
        unique=True
    )
    password = models.CharField(
        max_length=50,
        blank=False,
        unique=True
    )
    dob = models.DateField(
        max_length=50, null=True
    )

    def __str__(self):
        return 'name:'+self.name +' '+ 'password:'+self.password

class WebpageModel(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=False,
        unique=True)
    url = models.CharField(max_length=200, blank=False,
        unique=True)
    background_img = models.ImageField(blank=False)

    def __str__(self):
        return 'title:'+self.title 

class ContentModel(models.Model):
    website = models.ForeignKey(WebpageModel, on_delete=models.CASCADE)
    image = models.ImageField(blank=False,
        unique=True)
    title = models.CharField(max_length=50, default='Title', blank=False,
        unique=True)
    body = models.TextField(max_length=6000, blank=False,
        unique=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return 'title:'+self.title 

    class Meta:
        ordering = ['-created']


class LikeModel(models.Model):
    content = models.OneToOneField(ContentModel, on_delete=models.CASCADE)
    is_liked = models.BooleanField()

class CommentModel(models.Model):
    content = models.ForeignKey(ContentModel, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    name = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)