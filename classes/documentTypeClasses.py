from classes.chartClasses import *
import itertools

class ChartDocument(Document):
    def __init__(self, name: str, charts: list[Chart]):
        self.charts = [i.drawn() for i in charts]
        super().__init__(f'www/chart/{name}.html', default_basis,
                         list(itertools.chain(*[
                             groupGCharts(self.charts)['head']
                         ])),
                         list(itertools.chain(*[
                             [HTMLTag('div', CLASS='container', id='chart_container').adopted(groupGCharts(self.charts)['body'])]
                         ])))

class ArticleDocument(Document):
    def __init__(self, name: str, content: str):
        super().__init__(f'www/{name}.html', default_basis,[],
                         list(itertools.chain(*[
                             [HTMLTag('p', content)]
                         ])))
