from django.db import models

# Create your models here.
class AiModel(models.Model):
    
    ai_file = models.FileField(blank=True, unique=True) 
    

class Result(models.Model): 
    
    input = models.CharField(max_length = 128,verbose_name = '입력 텍스트',blank = True)
    result = models.TextField(verbose_name = '출력 장소', blank = True) 


class Place(models.Model):
    
    place_name = models.CharField(max_length = 128, unique=True,verbose_name='장소 이름',primary_key=True)
    place_address = models.TextField(verbose_name = '장소 주소',blank=True)
    place_latitude = models.FloatField(verbose_name='위도')
    place_longitude = models.FloatField(verbose_name='경도')
    place_phone = models.TextField(verbose_name='전화번호',blank = True)
    
    def __str__(self):
        return self.place_name


