from django.db import models

# Create your models here.

class Post(models.Model):

    title = models.CharField(max_length=50)
    desc = models.TextField()

    

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("Post_detail", kwargs={"pk": self.pk})
