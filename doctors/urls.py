from django.urls import path
from .views import doctor_list, doctor_detail


urlpatterns = [
    path('', doctor_list, name='doctor-list'),
    path('<int:pk>/', doctor_detail, name='doctor-detail'),
]