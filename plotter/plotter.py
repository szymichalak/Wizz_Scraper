import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import extra_data.functions as func
from extra_data.months import months as m


def get_months(data):
    months = []
    for item in data:
        if int(item[0][5:7]) not in months:
            months.append(int(item[0][5:7]))
    return months


class Plotter:
    def __init__(self, year, average):
        self.year = year
        self.average = average

    def create_plot(self, data):
        if self.year:
            visible = 30
            dates, prices = func.split_data(data)
            plt.plot(dates, prices)
            ax = plt.gca()
            temp = ax.xaxis.get_ticklabels()
            temp = list(set(temp) - set(temp[::visible]))
            for i, tic in enumerate(ax.xaxis.get_major_ticks()):
                tic.set_visible(False)
                if i % visible == 0:
                    tic.set_visible(True)
            for label in temp:
                label.set_visible(False)
            plt.show()

        if self.average:
            months_no = get_months(data)
            months_names = []
            for num in months_no:
                for key, value in m.items():
                    if num == value:
                        months_names.append(key)
            months_list = func.split_to_months(data)
            if [] in months_list:
                months_list.remove([])
            averages = []
            for one_month in months_list:
                averages.append(func.data_to_numpy(one_month).mean())
            fig, ax = plt.subplots()
            ax.plot(averages)

            labels = [item.get_text() for item in ax.get_xticklabels()]
            for i in range(len(labels)):
                if i != 1:
                    labels[i] = months_names[i]

            ax.set_xticklabels(labels)
            plt.show()
