from django import forms
from .models import Locations


class LocationsModelForm(forms.ModelForm):
    class Meta:
        model = Locations
        fields = ('name', 'state', 'review')
        
    def save(self, user, name, review, state, ide):
        obj = super().save(commit = False)
        obj.user = user
        obj.name = name
        obj.review = review
        obj.state = state
        obj.ide = ide
        obj.save()
        return obj
