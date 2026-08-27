from django.urls import path

from .views import department_list, department_detail


urlpatterns = [
    path('', department_list, name='department-list'),
    path('<int:pk>/', department_detail, name='department-detail'),
]