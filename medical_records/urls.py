from django.urls import path

from .views import medical_record_list, medical_record_detail


urlpatterns = [
    path('', medical_record_list, name='medical-record-list'),
    path(
        '<int:pk>/',
        medical_record_detail,
        name='medical-record-detail'
    ),
]