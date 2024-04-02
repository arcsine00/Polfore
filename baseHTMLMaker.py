from __future__ import annotations
import re

class HTMLTag:
    def __init__(self, name: str, content: str = '', CLASS: str = '', **kwargs):
        self.tagType = name
        self.opener = f'<{name}'+f' class="{CLASS}"'*(not not CLASS)
        for att, cont in kwargs.items():
            self.opener += f' {att}="{cont}"'
        self.opener += '>'
        self.exiter = f'</{name}>'
        self.content = content
        self.text = f'{self.opener}{self.content}{self.exiter}'
        self.children = [self.content]

    def adopted(self, children: list[HTMLTag]):
        for child in children:
            self.children.append(child.text)
            self.content += f'\n{child.text}'
        self.text = f'{self.opener}{self.content}{self.exiter}'
        return self


class Stylesheet(HTMLTag):
    def __init__(self, cont: str, issrc: bool = False, **kwargs):
        super().__init__('link' * issrc + 'style' * (not issrc), cont * (not issrc), href=cont * issrc,
                         rel='stylesheet' * issrc, type='text/css', **kwargs)


class Script(HTMLTag):
    def __init__(self, cont: str, issrc: bool = False, **kwargs):
        super().__init__('script', cont * (not issrc), src=cont * issrc, type='text/javascript', **kwargs)


class Navbar(HTMLTag):
    def __init__(self, home_title: str, service_dict: dict[str, str], **kwargs):
        self.title = home_title
        self.service_names = list(service_dict.keys())
        self.service_links = list(service_dict.values())
        super().__init__('nav', CLASS='navbar navbar-expand navbar-dark', **kwargs)

    def __call__(self):
        return self.adopted([
            HTMLTag('a', f'{self.title}', CLASS='navbar-brand', href='/'),
            HTMLTag('button', CLASS='navbar-toggler', type='button',
                    data__toggle='collapse', data__target='#navbarSupportedContent',
                    aria__controls='navbarSupportedContent', aria__expanded='false',
                    aria__label='Toggle navigation').adopted([
                HTMLTag('span', CLASS='navbar-toggler-icon')
            ]),
            HTMLTag('div', CLASS='collapse navbar-collapse', id='navbarSupportedContent').adopted([
                HTMLTag('ul', CLASS='navbar-nav mr-auto').adopted(
                    [HTMLTag('li', CLASS='nav-item').adopted([
                         HTMLTag('a', f'{name}', CLASS='nav-link', href=f'{link}')
                     ]) for name, link in zip(self.service_names, self.service_links)]
                )
            ])
        ])


def createGChart(chart: str, data: list, divid: str, title: str = '', width: int = 80, height: int = 500):
    s = f'''google.charts.load('current', {{'packages':['corechart']}});
    google.charts.setOnLoadCallback(draw_{divid});
    function draw_{divid}() {{
        var data = new google.visualization.arrayToDataTable({data});
        var options = {{
            title: '{title}'
        }};
        var chart = new google.visualization.{chart}Chart(document.getElementById('{divid}'));
        chart.draw(data, options);
    }}'''
    return [Script(s), HTMLTag('div', id=divid, style=f'width:{width}%; height:{height}px; border: 1px solid #ccc')]


def groupGCharts(charts: list[list]):
    return {'head': [Script('https://www.gstatic.com/charts/loader.js', True)] + [i[0] for i in charts],
            'body': [i[1] for i in charts]}


default_basis = {'head': [HTMLTag('meta', charset='utf-8'),
                  HTMLTag('title', 'Polfore'),
                  Stylesheet(
                      'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css',
                      True,
                      integrity='sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH',
                      crossorigin='anonymous'),
                  Script(
                      'https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js',
                      True,
                      integrity='sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz',
                      crossorigin='anonymous')
                  ],
         'body': [
             Navbar('폴포어', {
                 '홈': '/index.html',
                 '빅데이터 지지율': '/chart/partyApprovalRatings.html'
             })()
         ]}


class Document:
    def __init__(self, name: str, basis: dict, head: list[HTMLTag], body: list[HTMLTag]):
        self.name = name
        self.head = basis['head'] + head
        self.body = basis['body'] + body
        self.HTML = '<!DOCTYPE html>\n<html>\n'
        self.HTML += HTMLTag('head').adopted(self.head).text
        self.HTML += '\n'
        self.HTML += HTMLTag('body').adopted(self.body).text
        self.HTML += '</html>'
        self.HTML = re.sub(' [a-z]+="" ', ' ', self.HTML)
