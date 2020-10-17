from django.db import models
from django.utils.html import format_html
# Create your models here.
class Thammart(models.Model):
    status = [
        ('food','Food'),
        ('closet', 'Closet'),
        ('accessary', 'Accessary'),
        ('beauty', 'Beauty'),
        ('electronic', 'Electronic'),
        ('others','Others'),
    ]
    t_user = models.CharField(max_length=10)
    t_name = models.CharField(max_length=50)
    t_detail = models.CharField(max_length=200)
    t_cat = models.CharField(max_length=20, choices=status)

    def __str__(self) :
        return f"{self.t_user} : {self.t_name} {self.t_detail} {self.t_cat} "

class Profile(models.Model):
    p_user = models.CharField(max_length=10)
    p_name = models.CharField(max_length=50)
    p_sname = models.CharField(max_length=50)
    p_mail = models.CharField(max_length=40)
    p_channel = models.CharField(max_length=40)
    p_fav = models.ManyToManyField(Thammart, blank=True , related_name="favorites")
    p_mymart = models.ManyToManyField(Thammart, blank=True , related_name="mymart")

    def __str__(self) :
        return f"{self.p_user} : {self.p_name} {self.p_sname} {self.p_mail} {self.p_channel}"


