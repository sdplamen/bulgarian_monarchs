from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rulers.models import Monarch, Capital
from rulers.serializers import MonarchSerializer, CapitalSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class MonarchByYearView(APIView) :
    @swagger_auto_schema(
        operation_description="Retrieve the monarch who ruled Bulgaria in a specific year.",
        manual_parameters=[
            openapi.Parameter(
                'year', openapi.IN_QUERY, description="Year to search for a monarch", type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200 :openapi.Response(
                description="Monarch found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message' :openapi.Schema(type=openapi.TYPE_STRING),
                        'data' :MonarchSerializer()
                    }
                )
            ),
            400 :openapi.Response(description="Invalid year provided"),
            404 :openapi.Response(description="No monarch found for the year")
        }
    )
    def get(self, request) :
        year = request.query_params.get('year')
        try :
            year = int(year)
            monarch = Monarch.objects.filter(start_year__lte=year, end_year__gte=year).first()
            if monarch :
                serializer = MonarchSerializer(monarch)
                return Response({
                    'message' :f'The monarch in {monarch.start_year} to {monarch.end_year} was {monarch.name}. '
                               f'Governed from {monarch.capital.name if monarch.capital else "No capital assigned"}.',
                    'data' :serializer.data
                }, status=status.HTTP_200_OK)
            return Response({'message' :'Bulgaria had no such monarch for this year.'},
                            status=status.HTTP_404_NOT_FOUND)
        except (ValueError, TypeError) :
            return Response({'message' :'Please enter a valid year.'}, status=status.HTTP_400_BAD_REQUEST)


class MonarchByNameView(APIView) :
    @swagger_auto_schema(
        operation_description="Search for monarchs by name (case-insensitive).",
        manual_parameters=[
            openapi.Parameter(
                'name', openapi.IN_QUERY, description="Name or partial name of the monarch", type=openapi.TYPE_STRING
            )
        ],
        responses={
            200 :openapi.Response(
                description="Monarch(s) found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message' :openapi.Schema(type=openapi.TYPE_ARRAY,
                                                  items=openapi.Schema(type=openapi.TYPE_STRING)),
                        'data' :openapi.Schema(type=openapi.TYPE_ARRAY, items=MonarchSerializer())
                    }
                )
            ),
            400 :openapi.Response(description="Name parameter missing"),
            404 :openapi.Response(description="No monarchs found with the given name")
        }
    )
    def get(self, request) :
        name = request.query_params.get('name')
        if not name :
            return Response({'message' :'Please provide a name.'}, status=status.HTTP_400_BAD_REQUEST)

        monarchs = Monarch.objects.filter(name__icontains=name)
        if monarchs.exists() :
            serializer = MonarchSerializer(monarchs, many=True)
            return Response({
                'message' :[f'In {monarch.start_year} to {monarch.end_year} has governed {monarch.name}. '
                            f'Governed from {monarch.capital.name if monarch.capital else "No capital assigned"}.'
                            for monarch in monarchs],
                'data' :serializer.data
            }, status=status.HTTP_200_OK)
        return Response({'message' :['Bulgaria had no such monarch with this name.']}, status=status.HTTP_404_NOT_FOUND)


class CapitalByYearView(APIView) :
    @swagger_auto_schema(
        operation_description="Retrieve the capital of Bulgaria for a specific year.",
        manual_parameters=[
            openapi.Parameter(
                'year', openapi.IN_QUERY, description="Year to search for a capital", type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200 :openapi.Response(
                description="Capital found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message' :openapi.Schema(type=openapi.TYPE_STRING),
                        'data' :CapitalSerializer()
                    }
                )
            ),
            400 :openapi.Response(description="Invalid year provided"),
            404 :openapi.Response(description="No capital found for the year")
        }
    )
    def get(self, request) :
        year = request.query_params.get('year')
        try :
            year = int(year)
            capital = Capital.objects.filter(start_year__lte=year, end_year__gte=year).first()
            if capital :
                serializer = CapitalSerializer(capital)
                return Response({
                    'message' :f'In {capital.start_year} to {capital.end_year} Bulgaria was governed in {capital.name}.',
                    'data' :serializer.data
                }, status=status.HTTP_200_OK)
            return Response({'message' :'There is no capital found for this year.'}, status=status.HTTP_404_NOT_FOUND)
        except (ValueError, TypeError) :
            return Response({'message' :'Please enter a valid year.'}, status=status.HTTP_400_BAD_REQUEST)


class AddMonarchView(APIView) :
    @swagger_auto_schema(
        operation_description="Add a new monarch to the database, assigning a capital from the same period.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'start_year', 'end_year'],
            properties={
                'name' :openapi.Schema(type=openapi.TYPE_STRING, description="Name of the monarch"),
                'start_year' :openapi.Schema(type=openapi.TYPE_INTEGER, description="Start year of the monarch's rule"),
                'end_year' :openapi.Schema(type=openapi.TYPE_INTEGER, description="End year of the monarch's rule")
            }
        ),
        responses={
            201 :openapi.Response(
                description="Monarch created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message' :openapi.Schema(type=openapi.TYPE_STRING),
                        'data' :MonarchSerializer()
                    }
                )
            ),
            400 :openapi.Response(description="Invalid input or monarch already exists for the period"),
            404 :openapi.Response(description="No suitable capital found for the period")
        }
    )
    def post(self, request) :
        name = request.data.get('name')
        start_year = request.data.get('start_year')
        end_year = request.data.get('end_year')

        try :
            start_year = int(start_year)
            end_year = int(end_year)

            if Monarch.objects.filter(start_year=start_year, end_year=end_year).exists() :
                return Response({'message' :'A monarch already exists for this period.'},
                                status=status.HTTP_400_BAD_REQUEST)

            capital = Capital.objects.filter(start_year__lte=start_year, end_year__gte=end_year).first()
            if not capital :
                return Response({'message' :'No suitable capital found for this period.'},
                                status=status.HTTP_400_BAD_REQUEST)

            monarch = Monarch.objects.create(name=name, start_year=start_year, end_year=end_year, capital=capital)
            serializer = MonarchSerializer(monarch)
            return Response({
                'message' :f'Monarch {name} added for the period {start_year}-{end_year}. Assigned to capital {capital.name}.',
                'data' :serializer.data
            }, status=status.HTTP_201_CREATED)
        except ValueError :
            return Response({'message' :'Please enter valid years.'}, status=status.HTTP_400_BAD_REQUEST)