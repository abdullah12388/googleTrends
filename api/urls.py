from django.urls import path
from api import views as view


urlpatterns = [
    path('', view.google_trend_data, name='index'),
    path('h/<int:id>', view.HistoricalInterestApiView.as_view()),
    path('r/<int:id>', view.RegionInterestApiView.as_view()),
    path('charts', view.charts, name='charts')
]
