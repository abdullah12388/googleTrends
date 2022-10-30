from django.db import models

# Create your models here.


class SearchKey(models.Model):
    search_keyword = models.CharField(max_length=100)


class HistoricalInterest(models.Model):
    search_keyword = models.ForeignKey(SearchKey, on_delete=models.CASCADE)
    number_of_interest = models.IntegerField()
    time_stamp = models.DateTimeField(auto_now=None, auto_now_add=None)

    def __str__(self):
        return str(self.search_keyword) + str(self.time_stamp) + str(self.number_of_interest)


class RegionInterest(models.Model):
    search_keyword = models.ForeignKey(SearchKey, on_delete=models.CASCADE)
    region_name = models.CharField(max_length=100)
    region_interest = models.IntegerField()
    region_geo_code = models.CharField(max_length=10, default=None)

    def __str__(self):
        return str(self.search_keyword) + str(self.region_name) + str(self.region_interest)
