from django import forms

from .models import *


class AccommodationForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = ('name', 'location', 'introduce',
                  'built_time', 'remodeled_time', 'check_franchise',
                  'check_new_or_remodeling', 'introduce', 'service_kinds',
                  'service_introduce', 'service_notice', 'pickup_notice')


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='')
    class Meta:
        model = Image
        fields = ('image',)


class ReservationForm(forms.ModelForm):
    pass
