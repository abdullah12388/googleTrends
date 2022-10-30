from django.contrib import admin
from api.models import SearchKey, HistoricalInterest, RegionInterest


@admin.register(SearchKey)
class SearchKeyAdmin(admin.ModelAdmin):
    list_display = ['search_keyword']


@admin.register(HistoricalInterest)
class HistoricalInterestAdmin(admin.ModelAdmin):
    list_display = ['search_keyword', 'number_of_interest', 'time_stamp']


@admin.register(RegionInterest)
class RegionInterestAdmin(admin.ModelAdmin):
    list_display = ['search_keyword', 'region_name', 'region_interest']
