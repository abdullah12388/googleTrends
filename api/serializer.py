from rest_framework import serializers
from api.models import HistoricalInterest, RegionInterest


class HistoricalInterestSerializers(serializers.ModelSerializer):
    class Meta:
        model = HistoricalInterest
        fields = ['time_stamp', 'number_of_interest']


class RegionInterestSerializers(serializers.ModelSerializer):
    class Meta:
        model = RegionInterest
        fields = ['region_geo_code', 'region_name', 'region_interest']
