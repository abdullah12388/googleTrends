from django.shortcuts import render
from django.http import HttpResponseRedirect
from pytrends.request import TrendReq
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import SearchKey, HistoricalInterest, RegionInterest
from api.serializer import HistoricalInterestSerializers, RegionInterestSerializers


def historical_interest(kw_list):
    pytrends = TrendReq()
    kw_list = kw_list
    sk_id = SearchKey.objects.filter(search_keyword=kw_list[0])
    if sk_id.exists():
        sk_id = sk_id.first()
        if not HistoricalInterest.objects.filter(search_keyword=sk_id).exists():
            pytrends.build_payload(kw_list, cat=0, geo='', gprop='', timeframe='today 1-m')
            get_historical_interest = pytrends.get_historical_interest(kw_list, year_start=2022, month_start=1,
                                                                       day_start=1, hour_start=0,
                                                                       year_end=2022, month_end=2, day_end=1,
                                                                       hour_end=0, cat=0, geo='',
                                                                       gprop='', sleep=0)
            get_historical_interest_dict = get_historical_interest.to_dict(orient='dict')
            historical_list = []
            # print(get_historical_interest_dict)
            for k, v in get_historical_interest_dict[kw_list[0]].items():
                his_int = HistoricalInterest()
                his_int.search_keyword = sk_id
                his_int.time_stamp = k
                his_int.number_of_interest = v
                historical_list.append(his_int)
            HistoricalInterest.objects.bulk_create(historical_list)
            return get_historical_interest_dict
        else:
            return 'Exists'


def region_interest(kw_list):
    pytrends = TrendReq()
    kw_list = kw_list
    print(kw_list)
    sk_id = SearchKey.objects.filter(search_keyword=kw_list[0])
    if sk_id.exists():
        sk_id = sk_id.first()
        if not RegionInterest.objects.filter(search_keyword=sk_id).exists():
            # print(kw_list)
            pytrends.build_payload(kw_list, cat=0, geo='US', gprop='', timeframe='today 1-m')
            interest_by_region = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True, inc_geo_code=True)
            # print(interest_by_region)
            interest_by_region_dict = interest_by_region.to_dict(orient='dict')
            # print(interest_by_region_dict)
            region_list = []
            for k, v in interest_by_region_dict[kw_list[0]].items():
                reg_int = RegionInterest()
                reg_int.search_keyword = sk_id
                reg_int.region_name = k
                reg_int.region_geo_code = interest_by_region_dict['geoCode'][k]
                reg_int.region_interest = v
                region_list.append(reg_int)
            RegionInterest.objects.bulk_create(region_list)
            return interest_by_region_dict
        else:
            return 'Exists'


def google_trend_data(request):
    content = {}
    return render(request, 'index.html', content)


class HistoricalInterestApiView(APIView):
    def get(self, request, id):
        model_data = HistoricalInterest.objects.filter(search_keyword=id)
        serialize_data = HistoricalInterestSerializers(model_data, many=True)
        return Response(serialize_data.data)


class RegionInterestApiView(APIView):
    def get(self, request, id):
        model_data = RegionInterest.objects.filter(search_keyword=id)
        serialize_data = RegionInterestSerializers(model_data, many=True)
        return Response(serialize_data.data)


def charts(request):
    if request.POST:
        request_query = dict(request.POST)
        kw_list = request_query['ky_wd']
        if not SearchKey.objects.filter(search_keyword=kw_list[0]):
            sk = SearchKey()
            sk.search_keyword = kw_list[0]
            sk.save()
        sk_id = SearchKey.objects.filter(search_keyword=kw_list[0]).values_list('id', flat=True)
        his_int_result = historical_interest(kw_list)
        reg_int_result = region_interest(kw_list)
        content = {
            'id': list(sk_id)[0],
            'iot': his_int_result,
            'ibr': reg_int_result,
        }
        return render(request, 'charts.html', content)
    else:
        return HttpResponseRedirect('/')
