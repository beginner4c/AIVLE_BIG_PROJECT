import os
from django.db import models
from django.conf import settings
from uuid import uuid4
from datetime import datetime
# Create your models here.
def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid4().hex
    return '/'.join(['upload_file/', ymd_path, uuid_name])
class Notice(models.Model):
    notice_choice= (

    ('서비스안내', '서비스안내'),

    ('점검안내', '점검안내'),

    ('약관안내', '약관안내'),

  )
    category = models.CharField(max_length=10, choices=notice_choice,verbose_name = '공지종류')
    register_date = models.DateField(auto_now_add=True, verbose_name='등록시간')
    title = models.TextField(max_length=128, verbose_name='제목')
    contents = models.TextField(verbose_name = '공지내용')
    writer = models.ForeignKey('user.User', on_delete=models.CASCADE,verbose_name= '작성자')
    hits = models.PositiveBigIntegerField(verbose_name='조회수',default =0)
    top_fixed = models.BooleanField(verbose_name='상단고정',default = False)
    notice_image = models.ImageField(verbose_name='공지이미지',blank = True,upload_to='nImg')
    
    
    def __str__(self):
        return self.title