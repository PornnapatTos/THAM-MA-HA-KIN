from django.contrib import admin
from .models import Profile, Thammart

# Register your models here.
class profileAdmin(admin.ModelAdmin):
    list_display = ("p_user","p_name","p_sname","p_mail","p_phone","p_facebook","p_instragram","p_line")
    # list_display = ("p_user","p_name","p_sname","p_mail")

class thammartAdmin(admin.ModelAdmin):
    list_display = ("t_user","t_name","t_detail")

admin.site.register(Profile, profileAdmin)
admin.site.register(Thammart, thammartAdmin)