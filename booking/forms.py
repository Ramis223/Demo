from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking
from datetime import date

class RegisterForm(UserCreationForm):
    fio = forms.CharField(max_length=200, label='ФИО')
    phone = forms.CharField(max_length=20, label='Телефон')
    password1 = forms.CharField(min_length=8, label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'fio', 'phone', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 6:
            raise forms.ValidationError('Логин должен быть не менее 6 символов')
        return username

class BookingForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=['%d.%m.%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'ДД.ММ.ГГГГ'})
    )

    class Meta:
        model = Booking
        fields = ['hall', 'date', 'payment']

    def clean_date(self):
        booking_date = self.cleaned_data.get('date')
        if booking_date < date.today():
            raise forms.ValidationError('Дата не может быть в прошлом')
        return booking_date

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['review']
        widgets = {
            'review': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Напишите ваш отзыв...'})
        }
        