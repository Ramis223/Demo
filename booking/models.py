from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

class Hall(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название помещения')
    capacity = models.IntegerField(default=50, verbose_name='Вместимость')

    class Meta:
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('scheduled', 'Мероприятие назначено'),
        ('completed', 'Мероприятие завершено'),
    ]
    PAYMENT_CHOICES = [
        ('cash', 'Наличными'),
        ('card', 'По карте'),
        ('transfer', 'Безналичный'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name='Помещение')
    date = models.DateField(verbose_name='Дата начала')
    payment = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name='Способ оплаты')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    review = models.TextField(blank=True, null=True, verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f"{self.user.username} - {self.hall.name}"

    def can_leave_review(self):
        return self.status == 'completed'