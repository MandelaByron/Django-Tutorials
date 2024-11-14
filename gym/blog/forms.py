from django import forms
from .models import Blog
from tinymce.widgets import TinyMCE
class BlogCreateForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['title','category' , 'content',"thumbnail",'status' , 'tags']
        widgets = {'content': TinyMCE(attrs={'cols': 80, 'rows': 30})}