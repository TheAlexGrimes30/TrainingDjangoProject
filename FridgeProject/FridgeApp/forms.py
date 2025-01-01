from django import forms

from FridgeApp.models import Fridge, FridgeImage


class FridgeForm(forms.ModelForm):
    class Meta:
        model = Fridge
        fields = ['brand', 'model', 'description', 'price', 'capacity']
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter brand'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter model'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter capacity'}),
        }
        error_messages = {
            'brand': {
                'required': 'Please enter a brand for the fridge.',
                'max_length': 'The brand name is too long.',
            },
            'model': {
                'required': 'Please enter a model for the fridge.',
                'max_length': 'The model name is too long.',
            },
            'price': {
                'required': 'Please enter the price of the fridge.',
                'invalid': 'Please enter a valid price.',
            },
            'capacity': {
                'required': 'Please enter the capacity of the fridge.',
                'invalid': 'Please enter a valid capacity.',
            },
        }

class FridgeImageForm(forms.ModelForm):
    class Meta:
        model = FridgeImage
        fields = ['image', 'alt_text']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'id': 'id_image'}),
            'alt_text': forms.TextInput(attrs={'id': 'id_alt_text'}),
        }
        error_messages = {
            'image': {
                'required': 'Please add new image with formats (.jpg, .jpeg, .png)',
                'invalid': 'Please add valid image',
            },

            'alt_text': {
                'required': 'Please enter the alternative name',
                'max_length': 'The alternative name is too long.',
            },
        }
