from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from drf_spectacular.utils import extend_schema

from accounts.permissions import IsAdminOrReadOnly

from .models import Department
from .serializers import DepartmentSerializer


@extend_schema(
    methods=['GET'],
    operation_id='department_list',
    responses=DepartmentSerializer(many=True)
)
@extend_schema(
    methods=['POST'],
    operation_id='department_create',
    request=DepartmentSerializer,
    responses=DepartmentSerializer
)
@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
def department_list(request):

    departments = Department.objects.all()

    search = request.GET.get('search')

    if search:
        departments = departments.filter(
            name__icontains=search
        )

    available = request.GET.get('available')

    if available is not None:

        if available.lower() == 'true':
            departments = departments.filter(
                available=True
            )

        elif available.lower() == 'false':
            departments = departments.filter(
                available=False
            )

    floor = request.GET.get('floor')

    if floor:
        departments = departments.filter(
            floor=floor
        )

    if request.method == 'GET':

        paginator = PageNumberPagination()
        paginator.page_size = 5

        result_page = paginator.paginate_queryset(
            departments,
            request
        )

        serializer = DepartmentSerializer(
            result_page,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )

    serializer = DepartmentSerializer(
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
    operation_id='department_detail',
    responses=DepartmentSerializer
)
@extend_schema(
    methods=['PUT'],
    operation_id='department_update',
    request=DepartmentSerializer,
    responses=DepartmentSerializer
)
@extend_schema(
    methods=['DELETE'],
    operation_id='department_delete',
    responses=None
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def department_detail(request, pk):

    try:
        department = Department.objects.get(pk=pk)

    except Department.DoesNotExist:

        return Response(
            {'error': 'Department not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':

        serializer = DepartmentSerializer(department)

        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = DepartmentSerializer(
            department,
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

        department.delete()

        return Response(
            {'message': 'Department deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )