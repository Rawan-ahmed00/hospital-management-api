from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from drf_spectacular.utils import extend_schema

from accounts.permissions import IsAdminOrReadOnly

from .models import Patient
from .serializers import PatientSerializer


@extend_schema(
    methods=['GET'],
    operation_id='patient_list',
    responses=PatientSerializer(many=True)
)
@extend_schema(
    methods=['POST'],
    operation_id='patient_create',
    request=PatientSerializer,
    responses=PatientSerializer
)
@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
def patient_list(request):

    patients = Patient.objects.all()

    search = request.GET.get('search')

    if search:
        patients = patients.filter(
            name__icontains=search
        )

    phone = request.GET.get('phone')

    if phone:
        patients = patients.filter(
            phone__icontains=phone
        )

    gender = request.GET.get('gender')

    if gender:
        patients = patients.filter(
            gender__iexact=gender
        )

    doctor = request.GET.get('doctor')

    if doctor:
        patients = patients.filter(
            doctor_id=doctor
        )

    if request.method == 'GET':

        paginator = PageNumberPagination()
        paginator.page_size = 5

        result_page = paginator.paginate_queryset(
            patients,
            request
        )

        serializer = PatientSerializer(
            result_page,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )

    serializer = PatientSerializer(
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
    operation_id='patient_detail',
    responses=PatientSerializer
)
@extend_schema(
    methods=['PUT'],
    operation_id='patient_update',
    request=PatientSerializer,
    responses=PatientSerializer
)
@extend_schema(
    methods=['DELETE'],
    operation_id='patient_delete',
    responses=None
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def patient_detail(request, pk):

    try:
        patient = Patient.objects.get(pk=pk)

    except Patient.DoesNotExist:

        return Response(
            {'error': 'Patient not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':

        serializer = PatientSerializer(patient)

        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = PatientSerializer(
            patient,
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

        patient.delete()

        return Response(
            {'message': 'Patient deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )