from django import forms

from .models import ConversationMessage

class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model =  ConversationMessage
        fields = ('content',)
        # widget = {
        #     'content': forms.CharField(attrs={
        #         'class':'w-full py-4 px-6 rounded-xl border'
        #     })
        # }
    content = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Message...',
        'class' : 'w-full py-4 px-6 rounded-xl border'
    }))