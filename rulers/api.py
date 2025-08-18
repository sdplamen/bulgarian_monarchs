from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, inline_serializer
from rest_framework import serializers
from rulers.models import Monarch, Capital
from rulers.serializers import MonarchSerializer, CapitalSerializer

class MonarchByYearView(APIView):
    @extend_schema(
        description="Retrieve the monarch who ruled Bulgaria in a specific year.",
        parameters=[
            OpenApiParameter(
                'year',
                OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Year to search for a monarch"
            )
        ],
        responses={
            200: inline_serializer( # Using inline_serializer for structured response
                name='MonarchByYearResponse',
                fields={
                    'message': serializers.CharField(help_text="Response message"),
                    'data': MonarchSerializer(), # This is a serializer instance because it's a field within the inline_serializer
                }
            ),
            400: {'description': "Invalid year provided"},
            404: {'description': "No monarch found for the year"}
        }
    )
    def get(self, request):
        year = request.query_params.get('year')
        try:
            year = int(year)
            monarch = Monarch.objects.filter(start_year__lte=year, end_year__gte=year).first()
            if monarch:
                serializer = MonarchSerializer(monarch)
                return Response({
                    'message': f'The monarch in {monarch.start_year} to {monarch.end_year} was {monarch.name}. '
                               f'Governed from {monarch.capital.name if monarch.capital else "No capital assigned"}.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response({'message': 'Bulgaria had no such monarch for this year.'},
                            status=status.HTTP_404_NOT_FOUND)
        except (ValueError, TypeError):
            return Response({'message': 'Please enter a valid year.'}, status=status.HTTP_400_BAD_REQUEST)

class MonarchByNameView(APIView):
    @extend_schema(
        description="Search for monarchs by name (case-insensitive).",
        parameters=[
            OpenApiParameter(
                'name',
                OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Name or partial name of the monarch"
            )
        ],
        responses={
            200: inline_serializer( # Using inline_serializer for structured response
                name='MonarchByNameResponse',
                fields={
                    'message': serializers.ListField(child=serializers.CharField(), help_text="List of response messages"),
                    'data': MonarchSerializer(many=True), # Instance for a list of serializers
                }
            ),
            400: {'description': "Name parameter missing"},
            404: {'description': "No monarchs found with the given name"}
        }
    )
    def get(self, request):
        name = request.query_params.get('name')
        if not name:
            return Response({'message': 'Please provide a name.'}, status=status.HTTP_400_BAD_REQUEST)

        monarchs = Monarch.objects.filter(name__icontains=name)
        if monarchs.exists():
            serializer = MonarchSerializer(monarchs, many=True)
            return Response({
                'message': [f'In {monarch.start_year} to {monarch.end_year} has governed {monarch.name}. '
                            f'Governed from {monarch.capital.name if monarch.capital else "No capital assigned"}.'
                            for monarch in monarchs],
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({'message': ['Bulgaria had no such monarch with this name.']}, status=status.HTTP_404_NOT_FOUND)

class CapitalByYearView(APIView):
    @extend_schema(
        description="Retrieve the capital of Bulgaria for a specific year.",
        parameters=[
            OpenApiParameter(
                'year',
                OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Year to search for a capital"
            )
        ],
        responses={
            200: inline_serializer( # Using inline_serializer for structured response
                name='CapitalByYearResponse',
                fields={
                    'message': serializers.CharField(help_text="Response message"),
                    'data': CapitalSerializer(), # Instance as it's a field
                }
            ),
            400: {'description': "Invalid year provided"},
            404: {'description': "No capital found for the year"}
        }
    )
    def get(self, request):
        year = request.query_params.get('year')
        try:
            year = int(year)
            capital = Capital.objects.filter(start_year__lte=year, end_year__gte=year).first()
            if capital:
                serializer = CapitalSerializer(capital)
                return Response({
                    'message': f'In {capital.start_year} to {capital.end_year} Bulgaria was governed in {capital.name}.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response({'message': 'There is no capital found for this year.'}, status=status.HTTP_404_NOT_FOUND)
        except (ValueError, TypeError):
            return Response({'message': 'Please enter a valid year.'}, status=status.HTTP_400_BAD_REQUEST)

class AddMonarchView(APIView):
    @extend_schema(
        description="Add a new monarch to the database, assigning a capital from the same period.",
        request={
            'application/json': {
                'type': 'object',
                'required': ['name', 'start_year', 'end_year'],
                'properties': {
                    'name': {'type': 'string', 'description': "Name of the monarch"},
                    'start_year': {'type': 'integer', 'description': "Start year of the monarch's rule"},
                    'end_year': {'type': 'integer', 'description': "End year of the monarch's rule"}
                }
            }
        },
        responses={
            201: inline_serializer( # Using inline_serializer for structured response
                name='AddMonarchResponse',
                fields={
                    'message': serializers.CharField(help_text="Response message"),
                    'data': MonarchSerializer(), # Instance as it's a field
                }
            ),
            400: {'description': "Invalid input or monarch already exists for the period"},
            404: {'description': "No suitable capital found for the period"}
        }
    )
    def post(self, request):
        name = request.data.get('name')
        start_year = request.data.get('start_year')
        end_year = request.data.get('end_year')

        try:
            start_year = int(start_year)
            end_year = int(end_year)

            if Monarch.objects.filter(start_year=start_year, end_year=end_year).exists():
                return Response({'message': 'A monarch already exists for this period.'},
                                status=status.HTTP_400_BAD_REQUEST)

            capital = Capital.objects.filter(start_year__lte=start_year, end_year__gte=end_year).first()
            if not capital:
                return Response({'message': 'No suitable capital found for this period.'},
                                status=status.HTTP_400_BAD_REQUEST)

            monarch = Monarch.objects.create(name=name, start_year=start_year, end_year=end_year, capital=capital)
            serializer = MonarchSerializer(monarch)
            return Response({
                'message': f'Monarch {name} added for the period {start_year}-{end_year}. Assigned to capital {capital.name}.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        except ValueError:
            return Response({'message': 'Please enter valid years.'}, status=status.HTTP_400_BAD_REQUEST)
