from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        
        'username', 
        'name', 
        
        )
    search_fields = ('username', 'name')

admin.site.register(User, UserAdmin)
