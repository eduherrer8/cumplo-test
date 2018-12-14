# -*- coding: utf-8 -*-
import json

from django.conf import settings
from http.client import HTTPSConnection


class APICalls:

    conn = HTTPSConnection(settings.SERVER)
    headers = {
        'content-type': "application/json", 'bmx-token': settings.API_TOKEN
    }
    urls = {
        "time": "/SieAPIRest/service/v1/series/SP68257,SF60653/datos/{}/{}"
    }

    def time_function(self, date_start, date_end):
        new_url = self.urls["time"].format(
            date_start.strftime("%Y-%m-%d"), date_end.strftime("%Y-%m-%d"))
        self.conn.request("GET", new_url, "", self.headers)
        return self.to_representation()

    def to_representation(self):
        res = self.conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))["bmx"]


class AdjustInfo:

    def __init__(self, data):
        self.data = data

    def extra_info(self):
        aux = []
        for key in self.data["series"]:
            self.add_statistics(key)
        return self.data

    def add_statistics(self, serie):
        aux = [float(x["dato"]) for x in serie["datos"]]
        serie["Min"] = min(aux)
        serie["Max"] = max(aux)
        serie["average"] = sum(aux)/len(aux)
