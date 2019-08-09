from django import forms

from star_wars.models import Contestan


class ContestanAddForm(forms.ModelForm):

    class Meta:
        model = Contestan
        fields = ['first_name','last_name','date','phone','country','email']

    def __init__(self, *args, **kwargs):
        super(ContestanAddForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['id'] = 'contestan_date'
        self.fields['date'].widget.attrs['readonly'] = True
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

