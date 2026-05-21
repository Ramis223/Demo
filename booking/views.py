from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Booking, Hall
from .forms import RegisterForm, BookingForm, ReviewForm

class HomeView(TemplateView):
    template_name = 'home.html'

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Регистрация успешна!')
        return super().form_valid(form)

class LoginViewCustom(LoginView):
    template_name = 'login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Неверный логин или пароль')
        return super().form_invalid(form)

class CabinetView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'cabinet.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')

class BookingCreateView(LoginRequiredMixin, CreateView):
    form_class = BookingForm
    template_name = 'booking.html'
    success_url = reverse_lazy('cabinet')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Заявка отправлена на согласование!')
        return super().form_valid(form)

class AddReviewView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = ReviewForm
    template_name = 'add_review.html'
    success_url = reverse_lazy('cabinet')

    def dispatch(self, request, *args, **kwargs):
        booking = self.get_object()
        if not booking.can_leave_review():
            messages.error(request, 'Отзыв можно оставить только после завершения мероприятия')
            return redirect('cabinet')
        return super().dispatch(request, *args, **kwargs)

class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.username != 'Admin26':
            messages.error(request, 'Доступ только для администратора')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class AdminPanelView(AdminRequiredMixin, ListView):
    model = Booking
    template_name = 'admin_panel.html'
    context_object_name = 'bookings'
    paginate_by = 5

    def get_queryset(self):
        qs = Booking.objects.all().order_by('-created_at')
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_status'] = self.request.GET.get('status', '')
        return context

class AdminUpdateStatusView(AdminRequiredMixin, UpdateView):
    model = Booking
    fields = ['status']
    success_url = reverse_lazy('admin_panel')
    
    def form_valid(self, form):
        messages.success(self.request, 'Статус заявки обновлен')
        return super().form_valid(form)