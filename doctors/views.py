from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from drf_spectacular.utils import extend_schema

from accounts.permissions import IsAdminOrReadOnly

from .models import Doctor
from .serializers import DoctorSerializer


@extend_schema(
    methods=['GET'],
    operation_id='doctor_list',
    responses=DoctorSerializer(many=True)
)
@extend_schema(
    methods=['POST'],
    operation_id='doctor_create',
    request=DoctorSerializer,
    responses=DoctorSerializer
)
@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
def doctor_list(request):

    doctors = Doctor.objects.all()

    specialty = request.GET.get('specialty')

    if specialty:
        doctors = doctors.filter(
            specialty__iexact=specialty
        )

    available = request.GET.get('available')

    if available is not None:

        if available.lower() == 'true':
            doctors = doctors.filter(available=True)

        elif available.lower() == 'false':
            doctors = doctors.filter(available=False)

    search = request.GET.get('search')

    if search:
        doctors = doctors.filter(
            name__icontains=search
        )

    if request.method == 'GET':

        paginator = PageNumberPagination()
        paginator.page_size = 5

        result_page = paginator.paginate_queryset(
            doctors,
            request
        )

        serializer = DoctorSerializer(
            result_page,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )

    serializer = DoctorSerializer(
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
    operation_id='doctor_detail',
    responses=DoctorSerializer
)
@extend_schema(
    methods=['PUT'],
    operation_id='doctor_update',
    request=DoctorSerializer,
    responses=DoctorSerializer
)
@extend_schema(
    methods=['DELETE'],
    operation_id='doctor_delete',
    responses=None
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def doctor_detail(request, pk):

    try:
        doctor = Doctor.objects.get(pk=pk)

    except Doctor.DoesNotExist:

        return Response(
            {'error': 'Doctor not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':

        serializer = DoctorSerializer(doctor)

        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = DoctorSerializer(
            doctor,
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

        doctor.delete()

        return Response(
            {'message': 'Doctor deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )