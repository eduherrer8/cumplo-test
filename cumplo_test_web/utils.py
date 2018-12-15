# -*- coding: utf-8 -*-
import json
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

from django.conf import settings
from django.core.files import File
from http.client import HTTPSConnection

from cumplo_test_web.models import ImageHelper


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
        for key in self.data["series"]:
            self.add_statistics(key)
        return self.data

    def add_statistics(self, serie):
        aux = [float(x["dato"]) for x in serie["datos"]]
        serie["Min"] = min(aux)
        serie["Max"] = max(aux)
        serie["average"] = sum(aux)/len(aux)
        serie["graph"] = self.create_chart(aux, serie['idSerie'])

    def create_chart(self, data, title):
        objects = [str(x) for x in range(1, len(data)+1)]
        y_pos = np.arange(len(objects))
        plt.bar(y_pos, data, tick_label=data, color="grey")
        plt.xticks(y_pos, objects)
        plt.title(title)

        blob = BytesIO()
        plt.savefig(blob, format="png")

        plot_instance = ImageHelper()
        plot_instance.image.save('serie.jpg', File(blob), save=False)
        plot_instance.save()
        plt.clf()
        return plot_instance.image.url
