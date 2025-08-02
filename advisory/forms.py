from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from .models import Farmer, MalawiRegion, Crop

class FarmerRegistrationForm(forms.ModelForm):
    """Form for farmer registration"""
    
    class Meta:
        model = Farmer
        fields = ['phone_number', 'location', 'farm_size_acres', 'preferred_language', 'primary_crops']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '+265...'}),
            'farm_size_acres': forms.NumberInput(attrs={'step': '0.1', 'min': '0.1'}),
            'primary_crops': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-3'),
                Column('preferred_language', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('location', css_class='form-group col-md-6 mb-3'),
                Column('farm_size_acres', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Field('primary_crops', css_class='mb-3'),
            Submit('submit', _('Register'), css_class='btn btn-success btn-lg')
        )
        
        # Add help text
        self.fields['phone_number'].help_text = _('Enter your mobile phone number with country code')
        self.fields['farm_size_acres'].help_text = _('Approximate size of your farm in acres')
        self.fields['primary_crops'].help_text = _('Select the main crops you grow')

class FarmerProfileForm(forms.ModelForm):
    """Form for updating farmer profile"""
    
    class Meta:
        model = Farmer
        fields = ['phone_number', 'location', 'farm_size_acres', 'preferred_language', 'primary_crops']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '+265...'}),
            'farm_size_acres': forms.NumberInput(attrs={'step': '0.1', 'min': '0.1'}),
            'primary_crops': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-3'),
                Column('preferred_language', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('location', css_class='form-group col-md-6 mb-3'),
                Column('farm_size_acres', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Field('primary_crops', css_class='mb-3'),
            Submit('submit', _('Update Profile'), css_class='btn btn-primary btn-lg')
        )

class CropFilterForm(forms.Form):
    """Form for filtering crops"""
    region = forms.ModelChoiceField(
        queryset=MalawiRegion.objects.all(),
        required=False,
        empty_label=_('All Regions'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    crop_type = forms.ChoiceField(
        choices=[('', _('All Types'))] + Crop.CROP_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _('Search crops...'),
            'class': 'form-control'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('region', css_class='col-md-4'),
                Column('crop_type', css_class='col-md-4'),
                Column('search', css_class='col-md-4'),
                css_class='form-row'
            ),
            Submit('filter', _('Filter'), css_class='btn btn-primary')
        )