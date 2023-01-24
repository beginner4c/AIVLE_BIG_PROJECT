from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid 

from django.conf import settings  
from django.db import models
from django.core.mail import send_mail 
from django.utils.html import strip_tags 
from django.template.loader import render_to_string

class User(AbstractUser):
    
    username = models.CharField(max_length=20, verbose_name="아이디", unique=True,primary_key = True)
    email = models.EmailField(max_length = 30,verbose_name = '이메일',unique = True)
    password = models.CharField(max_length = 30,verbose_name= '비밀번호')
    name = models.CharField(max_length=30,verbose_name='이름')
    phone = models.CharField(max_length = 20, verbose_name= '연락처')
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default="", blank=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.username
    def verify_email(self): 
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20] 
            self.email_secret = secret  
            html_message = render_to_string(
                "verify_email.html", {"secret": secret}
            )
            send_mail(
                "Verify Traivler Account",  
                strip_tags(html_message),  
                settings.EMAIL_FROM,  
                [self.email],  
                fail_silently=False, 
                html_message=html_message,  
            )
            self.save() 
        return
