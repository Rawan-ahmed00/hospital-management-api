from django.urls import path

from .views import appointment_list, appointment_detail


urlpatterns = [
    path('', appointment_list, name='appointment-list'),
    path('<int:pk>/', appointment_detail, name='appointment-detail'),
]