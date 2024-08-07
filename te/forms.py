from django import forms
from django.forms import formset_factory
from django.core.exceptions import ValidationError
from te.models import Profile, PlantedTree

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about']

    widgets = {
            'about': forms.TextInput(attrs={'class': 'form-control'}),
     }
    
class PlantedTreeForm(forms.ModelForm):
    class Meta:
        model = PlantedTree
        fields = [ 'tree', 'age', 'account', 'latitude', 'longitude']
        widgets = {
            'tree': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'account': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'account': 'Active accounts',
        }
    
    def clean_age(self):
        age = self.cleaned_data['age']
        if age < 0:
            raise ValidationError("Age cannot be negative.")
        
        return age

PlantedTreeFormSet = formset_factory(PlantedTreeForm, max_num=10)

