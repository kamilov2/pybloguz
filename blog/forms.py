from django import forms 
from .models import Comment



class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('text','full_name')
        widgets = {
            'text':forms.Textarea(attrs={'rows':5, 'placeholder':'Fikr matni'}),
            'full_name':forms.TextInput(attrs={'placeholder':'Ism Familya', "style":'margin-bottom:10px;'})
        }