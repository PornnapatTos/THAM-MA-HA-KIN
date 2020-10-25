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
    t_count = models.PositiveIntegerField()
    t_price = models.CharField(max_length=10)
    t_image = models.CharField(max_length=1000)
    def __str__(self) :
        return f"{self.t_user} : {self.t_name} {self.t_price} {self.t_detail} {self.t_cat} {self.t_count} "

    # def __str__(self) :
    #     return f"{self.t_user} : {self.t_name} {self.t_detail} {self.t_cat}"

class Profile(models.Model):
    p_user = models.CharField(max_length=10)
    p_name = models.CharField(max_length=50)
    p_sname = models.CharField(max_length=50)
    p_mail = models.CharField(max_length=40)
    p_phone = models.CharField(max_length=40)
    p_facebook = models.CharField(max_length=40)
    p_instragram = models.CharField(max_length=40)
    p_line = models.CharField(max_length=40)
    p_fav = models.ManyToManyField(Thammart, blank=True , related_name="favorites")
    p_mymart = models.ManyToManyField(Thammart, blank=True , related_name="mymart")

    def __str__(self) :
        return f"{self.p_user} : {self.p_name} {self.p_sname} {self.p_phone} {self.p_mail} {self.p_instragram} {self.p_facebook} {self.p_line}"

    # def __str__(self) :
    #     return f"{self.p_user} : {self.p_name} {self.p_sname} {self.p_mail}"


