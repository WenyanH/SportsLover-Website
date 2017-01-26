from models import *
from django import forms
from django.contrib.auth.models import User
from datetime import date, datetime
from calendar import monthrange


class UserForm(forms.Form):    
    username = forms.CharField(max_length = 20,
                               widget=forms.TextInput(attrs={
                                    'class':'form-control', 
                                    'placeholder':'3-25 length of password with charaters, numbers, and !@#$%^*_|',
                                    'pattern':'[a-zA-Z0-9!@#$%^*_|]{3,25}'
                                }))
    first_name = forms.CharField(max_length = 20,
                                 widget=forms.TextInput(attrs={
                                    'class':'form-control', 
                                    'placeholder':'First Name'
                                }))
    last_name = forms.CharField(max_length = 20,
                                widget=forms.TextInput(attrs={
                                    'class':'form-control', 
                                    'placeholder':'Last Name'
                                }))
    email = forms.EmailField(max_length = 200, 
                             widget=forms.TextInput(attrs={
                                'class':'form-control', 
                                'placeholder':'Email'
                             }))
    password1 = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget = forms.PasswordInput(attrs={
                                    'class':'form-control', 
                                    'placeholder':'Password'
                                    }))
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm password',  
                                widget = forms.PasswordInput(attrs={
                                    'class':'form-control', 
                                    'placeholder':'Confirm Password'
                                    }))

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username


class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ['first_name', 'last_name', 'age', 'bio', 'image']
        widgets = {
            'first_name': forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'First Name'
                    }),
            'last_name': forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Last Name'
                    }),
            'age': forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Age'
                    }),
            'bio': forms.Textarea(attrs={
                        'class': 'form-control',
                        'rows': '2',
                        'placeholder': 'Short Bio'
                    }),
            'image': forms.FileInput()
            }

class GroupForm(forms.Form):
        subject = forms.CharField(max_length = 50,
                                  widget=forms.TextInput(attrs={
                                     'class':'form-control',
                                    'placeholder':'Group Subject'
                                }))
        sportsitem = forms.CharField(max_length = 40,
                                     widget=forms.TextInput(attrs={
                                    'class':'form-control',
                                    'placeholder':'Sports Item'
                                }))
        sportsclass = forms.CharField(max_length = 40,
                                      widget=forms.TextInput(attrs={
                                    'class':'form-control dropdown-toggle',
                                    'data-toggle':"dropdown",
                                    'placeholder':'Sports Class',
                                }))
        place = forms.CharField(max_length = 40,
                                widget=forms.TextInput(attrs={
                                    'class':'form-control',
                                    'placeholder':'Place'
                                }))
        address = forms.CharField(max_length = 100,
                                  widget=forms.Textarea(attrs={
                                    'class':'form-control',
                                    'rows':'2',
                                    'placeholder':'Detail Address'
                                }))
        cost = forms.DecimalField(max_digits=5,
                                  decimal_places=2,
                                  widget=forms.TextInput(attrs={
                                    'class':'form-control', 
                                    'placeholder':'0.00'
                                }))
        size = forms.IntegerField(
                               widget=forms.TextInput(attrs={
                                    'class':'form-control', 
                                    'placeholder':'1'
                                }))
        date_begin = forms.DateTimeField(input_formats=['%Y/%m/%d %H:%M'],
                               widget=forms.DateTimeInput(attrs={
                                    'class':'form-control  datetimepicker',
                                    'placeholder':'Start Time'
                                }))
        date_end = forms.DateTimeField(input_formats=['%Y/%m/%d %H:%M'],
                               widget=forms.DateTimeInput(attrs={
                                    'class':'form-control  datetimepicker',
                                    'placeholder':'End Time'
                                }))
        introduction = forms.CharField(max_length = 400,
                               widget=forms.Textarea(attrs={
                                    'class':'form-control',
                                    'rows':'2',
                                    'placeholder':'Introduction'
                                }))
        def clean(self):
            cleaned_data = super(GroupForm, self).clean()
            date_begin = cleaned_data.get('date_begin')
            date_end = cleaned_data.get('date_end')
            if date_end < date_begin:
                raise forms.ValidationError("Date:End date cannot be earlier then Start Date.")
            return cleaned_data


class PasswordForm(forms.Form):   
    password1 = forms.CharField(max_length=200,
                                label='Password', 
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Password'
                                    }))
    password2 = forms.CharField(max_length=200,
                                label='Confirm password',
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Confirm Password'
                                 }))

    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data
