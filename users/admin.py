from django.contrib import admin
from .models import Profile, Thammart

# Register your models here.
class profileAdmin(admin.ModelAdmin):
    list_display = ("p_user","p_name","p_sname","p_mail")
    # list_display = ("p_user","p_name","p_sname","p_mail")

class thammartAdmin(admin.ModelAdmin):
    list_display = ("t_user","t_name","t_detail","t_price","t_date","t_channel")

admin.site.register(Profile, profileAdmin)
admin.site.register(Thammart, thammartAdmin)