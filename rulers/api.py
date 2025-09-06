from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, inline_serializer
from rest_framework import serializers
from rulers.models import Monarch, Capital
from rulers.serializers import MonarchSerializer, CapitalSerializer

class MonarchByYearView(APIView):
    @extend_schema(
        description='Търсене на владетел, който е упранлянал през конкретна година.',
        parameters=[
            OpenApiParameter(
                'year',
                OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Година за търсене по владетел'
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
            400: {'description': 'Неправилно въведена година'},
            404: {'description': 'Няма намерен владетел за тази година'}
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
                    'message': f'Владетел през {monarch.start_year} до {monarch.end_year} бил {monarch.name} {monarch.family if monarch.family else ''}. '
                               f'Управлявал от {monarch.capital.name if monarch.capital else 'няма известна столица'}.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response({'message': 'България няма такъв владетел през тази година.'},
                            status=status.HTTP_404_NOT_FOUND)
        except (ValueError, TypeError):
            return Response({'message': 'Моля, въведи правилна година.'}, status=status.HTTP_400_BAD_REQUEST)

class MonarchByNameView(APIView):
    @extend_schema(
        description="Търсене на врадетел по име (case-insensitive).",
        parameters=[
            OpenApiParameter(
                'name',
                OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Име или част от име на владетеля"
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
            400: {'description': 'Липсващи данни за име'},
            404: {'description': "Няма намерен монарх с такова име"}
        }
    )
    def get(self, request):
        name = request.query_params.get('name')
        if not name:
            return Response({'message': 'моля, въведи име.'}, status=status.HTTP_400_BAD_REQUEST)

        monarchs = Monarch.objects.filter(name__icontains=name)
        if monarchs.exists():
            serializer = MonarchSerializer(monarchs, many=True)
            return Response({
                'message': [f'През {monarch.start_year} до {monarch.end_year} управлявавал {monarch.name} {monarch.family if monarch.family else ''}. '
                            f'Управлявал от {monarch.capital.name if monarch.capital else 'Няма известна столица'}.'
                            for monarch in monarchs],
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({'message': ['България няма владетел с такова име.']}, status=status.HTTP_404_NOT_FOUND)

class CapitalByYearView(APIView):
    @extend_schema(
        description='Търсене на столица на България по специфична година.',
        parameters=[
            OpenApiParameter(
                'year',
                OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Година за търсене по столица'
            )
        ],
        responses={
            200: inline_serializer( # Using inline_serializer for structured response
                name='CapitalByYearResponse',
                fields={
                    'message': serializers.CharField(help_text="Response message"),
                    'data': CapitalSerializer(),
                }
            ),
            400: {'description': 'Неправилно въведена година'},
            404: {'description': 'Няма столица за този период'}
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
                    'message': f'През {capital.start_year} до {capital.end_year} България била управляване от {capital.name}.',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response({'message': 'Няма известна столица за този период.'}, status=status.HTTP_404_NOT_FOUND)
        except (ValueError, TypeError):
            return Response({'message': 'Моля, въведи правилна година.'}, status=status.HTTP_400_BAD_REQUEST)

class AddMonarchView(APIView):
    @extend_schema(
        description='Добави нов владетел в базата данни, сато добавиш съответния род и столица да този период.',
        request={
            'application/json': {
                'type': 'object',
                'required': ['name', 'family', 'start_year', 'end_year'],
                'properties': {
                    'name': {'type': 'string', 'description': "Name of the monarch"},
                    'family': {'type': 'string', 'description': "Family of the monarch"},
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
            400: {'description': 'Неправилно въвеждане или владетелят вече съществува за този период'},
            404: {'description': 'Няма известна столица за този период'}
        }
    )
    def post(self, request):
        name = request.data.get('name')
        family = request.data.get('family')
        start_year = request.data.get('start_year')
        end_year = request.data.get('end_year')

        try:
            start_year = int(start_year)
            end_year = int(end_year)

            if Monarch.objects.filter(start_year=start_year, end_year=end_year).exists():
                return Response({'message': 'Вече съществува владетел за този период.'},
                                status=status.HTTP_400_BAD_REQUEST)

            capital = Capital.objects.filter(start_year__lte=start_year, end_year__gte=end_year).first()
            if not capital:
                return Response({'message': 'Няма подходяща столица за този период.'},
                                status=status.HTTP_400_BAD_REQUEST)

            monarch = Monarch.objects.create(name=name, family=family, start_year=start_year, end_year=end_year, capital=capital)
            serializer = MonarchSerializer(monarch)
            return Response({
                'message': f'Владетелят {name} {monarch.family if monarch.family else ''} е добавен за периода {start_year}-{end_year}. Със столиза на царуване {capital.name}.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        except ValueError:
            return Response({'message': 'Моля, въведете правилна година.'}, status=status.HTTP_400_BAD_REQUEST)
