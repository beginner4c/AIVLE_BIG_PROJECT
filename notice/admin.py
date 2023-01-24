from django.contrib import admin
from .models import Notice
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
class NoticeAdmin(SummernoteModelAdmin):
    summernote_fields = ('contents',)
    list_display = (
        'title',
        'register_date',
        'contents',
        'writer',
        'hits',
    )

admin.site.register(Notice,NoticeAdmin)
