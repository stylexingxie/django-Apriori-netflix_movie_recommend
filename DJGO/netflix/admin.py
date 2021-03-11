from django.contrib import admin
from .models import NetflixAll, NetflixOri


# Register your models here.


class NetflixAllAdmin(admin.ModelAdmin):
    search_fields = ['cast']


class NetflixOriAdmin(admin.ModelAdmin):
    search_fields = ['show_id']


admin.site.register(NetflixAll, NetflixAllAdmin)
admin.site.register(NetflixOri, NetflixOriAdmin)
