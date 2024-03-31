from baseHTMLMaker import *
import random
import numpy as np

class Chart:
    def __init__(self, raw_data: list[list], colors: list, labels: list, title: str = '', chartType: str = ''):
        self.data = raw_data
        self.colors = colors
        self.labels = labels
        self.title = title
        if chartType == 'Pie':
            self.is1D = True
        else:
            self.is1D = False
        self.chartType = chartType
        self.id = f'{self.chartType}Chart_{random.getrandbits(32)}'
    def drawn(self):
        if self.is1D:
            self.processed_data = [['label', 'data']]+[[self.labels[NO], n] for NO, n in enumerate(self.data[-1])]
        else:
            self.processed_data = [["no"]+self.labels] + [[NO]+arr for NO, arr in enumerate([(el/sum(el)*100).tolist() for el in np.array(self.data)])]
        return createGChart(self.chartType, self.processed_data, self.id, self.title)

class PieChart(Chart):
    def __init__(self, raw_data: list, colors: list, labels: list, title: str = ''):
        super().__init__(raw_data, colors, labels, title, 'Pie')

class LineChart(Chart):
    def __init__(self, raw_data: list, colors: list, labels: list, title: str = ''):
        super().__init__(raw_data, colors, labels, title, 'Line')
