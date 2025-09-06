from rest_framework import serializers
from rulers.models import Monarch, Capital

class MonarchSerializer(serializers.ModelSerializer):
    capital_name = serializers.CharField(source='capital.name', read_only=True, allow_null=True)

    class Meta:
        model = Monarch
        fields = ['name', 'family', 'start_year', 'end_year', 'capital_name']

class CapitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capital
        fields = ['name', 'family', 'start_year', 'end_year']