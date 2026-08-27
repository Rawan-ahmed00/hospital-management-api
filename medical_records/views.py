from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from drf_spectacular.utils import extend_schema

from accounts.permissions import IsAdminOrReadOnly

from .models import MedicalRecord
from .serializers import MedicalRecordSerializer


@extend_schema(
    methods=['GET'],
    operation_id='medical_record_list',
    responses=MedicalRecordSerializer(many=True)
)
@extend_schema(
    methods=['POST'],
    operation_id='medical_record_create',
    request=MedicalRecordSerializer,
    responses=MedicalRecordSerializer
)
@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
def medical_record_list(request):

    records = MedicalRecord.objects.all()

    patient = request.GET.get('patient')

    if patient:
        records = records.filter(
            patient_id=patient
        )

    doctor = request.GET.get('doctor')

    if doctor:
        records = records.filter(
            doctor_id=doctor
        )

    search = request.GET.get('search')

    if search:
        records = records.filter(
            diagnosis__icontains=search
        )

    record_date = request.GET.get('record_date')

    if record_date:
        records = records.filter(
            record_date=record_date
        )

    if request.method == 'GET':

        paginator = PageNumberPagination()
        paginator.page_size = 5

        result_page = paginator.paginate_queryset(
            records,
            request
        )

        serializer = MedicalRecordSerializer(
            result_page,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )

    serializer = MedicalRecordSerializer(
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
    operation_id='medical_record_detail',
    responses=MedicalRecordSerializer
)
@extend_schema(
    methods=['PUT'],
    operation_id='medical_record_update',
    request=MedicalRecordSerializer,
    responses=MedicalRecordSerializer
)
@extend_schema(
    methods=['DELETE'],
    operation_id='medical_record_delete',
    responses=None
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def medical_record_detail(request, pk):

    try:
        record = MedicalRecord.objects.get(
            pk=pk
        )

    except MedicalRecord.DoesNotExist:

        return Response(
            {
                'error': 'Medical record not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':

        serializer = MedicalRecordSerializer(
            record
        )

        return Response(
            serializer.data
        )

    elif request.method == 'PUT':

        serializer = MedicalRecordSerializer(
            record,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':

        record.delete()

        return Response(
            {
                'message': 'Medical record deleted successfully'
            },
            status=status.HTTP_204_NO_CONTENT
        )
          