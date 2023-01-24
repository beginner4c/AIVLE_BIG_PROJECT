from django import forms
from .models import Review
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget

class ReviewWriteForm(forms.ModelForm):
    title = forms.CharField(
        label = '리뷰 제목',
        widget = forms.TextInput(
            attrs = {
                'placeholder':'게시글 제목'
            }   
        ),
        required=True,
    )
    
    contents = SummernoteTextField()
    field_order = [
        'title',
        'contents'
    ]   
    class Meta:
        model = Review
        fields = [
            'title',
            'contents',
            
        ]
        widgets = {
            'contents' : SummernoteWidget()
            
        }
        
    title.widget.attrs['size'] = 80
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title','')
        contents = cleaned_data.get('contents','')
        
        if title == '':
            self.add_error('title','글 제목을 입력하세요.')
        elif contents =='':
            self.add_error('contents','글 내용을 입력하세요.') 
        else :
            self.title=title
            self.contents = contents
            