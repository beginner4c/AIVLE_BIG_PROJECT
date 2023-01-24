from django import forms
from .models import *

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['input','result']
        
class AiModelForm(forms.ModelForm):
    class Meta:
        model = AiModel
        fields = ['ai_file']
        
