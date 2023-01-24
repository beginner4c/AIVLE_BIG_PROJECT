import os
from django.db import models
from django.conf import settings
from uuid import uuid4

# Create your models here.

class Review(models.Model):
    writer = models.ForeignKey('user.User', on_delete=models.CASCADE,verbose_name= '작성자')
    register_date = models.DateField(auto_now_add=True, verbose_name='등록시간')
    title = models.TextField(max_length=128, verbose_name='리뷰제목')
    contents = models.TextField(verbose_name = '리뷰내용')
    hits = models.PositiveBigIntegerField(verbose_name='조회수',default =0)
    top_fixed = models.BooleanField(verbose_name='상단고정',default = False)
    review_image = models.ImageField(verbose_name='리뷰이미지',blank = True,upload_to='rImg')
    place = models.ForeignKey('ai.Place', on_delete=models.CASCADE,verbose_name= '장소')
    
    
    def __str__(self):
        return self.title
