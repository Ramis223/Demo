from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginViewCustom.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cabinet/', views.CabinetView.as_view(), name='cabinet'),
    path('booking/', views.BookingCreateView.as_view(), name='booking'),
    path('review/<int:pk>/', views.AddReviewView.as_view(), name='add_review'),
    path('admin/', views.AdminPanelView.as_view(), name='admin_panel'),
    path('admin/status/<int:pk>/', views.AdminUpdateStatusView.as_view(), name='admin_status'),
]