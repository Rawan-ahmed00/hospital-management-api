from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from drf_spectacular.utils import extend_schema

from accounts.permissions import IsAdminOrReadOnly

from .models import Appointment
from .serializers import AppointmentSerializer


@extend_schema(
    methods=['GET'],
    operation_id='appointment_list',
    responses=AppointmentSerializer(many=True)
)
@extend_schema(
    methods=['POST'],
    operation_id='appointment_create',
    request=AppointmentSerializer,
    responses=AppointmentSerializer
)
@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
def appointment_list(request):

    appointments = Appointment.objects.all()

    doctor = request.GET.get('doctor')

    if doctor:
        appointments = appointments.filter(
            doctor_id=doctor
        )

    patient = request.GET.get('patient')

    if patient:
        appointments = appointments.filter(
            patient_id=patient
        )

    appointment_status = request.GET.get('status')

    if appointment_status:
        appointments = appointments.filter(
            status__iexact=appointment_status
        )

    date = request.GET.get('date')

    if date:
        appointments = appointments.filter(
            date=date
        )

    if request.method == 'GET':

        paginator = PageNumberPagination()
        paginator.page_size = 5

        result_page = paginator.paginate_queryset(
            appointments,
            request
        )

        serializer = AppointmentSerializer(
            result_page,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )

    serializer = AppointmentSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@extend_schema(
    methods=['GET'],
    operation_id='appointment_detail',
    responses=AppointmentSerializer
)
@extend_schema(
    methods=['PUT'],
    operation_id='appointment_update',
    request=AppointmentSerializer,
    responses=AppointmentSerializer
)
@extend_schema(
    methods=['DELETE'],
    operation_id='appointment_delete',
    responses=None
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def appointment_detail(request, pk):

    try:
        appointment = Appointment.objects.get(pk=pk)

    except Appointment.DoesNotExist:

        return Response(
            {'error': 'Appointment not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':

        serializer = AppointmentSerializer(
            appointment
        )

        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = AppointmentSerializer(
            appointment,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':

        appointment.delete()

        return Response(
            {'message': 'Appointment deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )