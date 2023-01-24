from django.contrib import admin
from .models import Review
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.
class ReviewAdmin(SummernoteModelAdmin):
    summernote_fields = ('contents',)
    list_display = (
        'title',
        'register_date',
        'place',
        'contents',
        'writer',
        'hits',
    )

admin.site.register(Review,ReviewAdmin)

