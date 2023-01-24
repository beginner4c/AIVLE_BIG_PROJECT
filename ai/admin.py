from django.contrib import admin
from .models import Result, AiModel
# Register your models here.
class ResultAdmin(admin.ModelAdmin):
    list_display = ['input','result']
admin.site.register(Result, ResultAdmin)

class AiModelAdmin(admin.ModelAdmin):

    list_display = ['ai_file']

admin.site.register(AiModel, AiModelAdmin)