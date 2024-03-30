import requests
import json
import time
import matplotlib.pyplot as plt
import itertools

import init
import calc
import baseHTMLMaker as ht

def newFile(graphee, file):
    if not graphee:
        for i in init.party_space:
            graphee[i] = []
        graphee["기준"] = 0
    if not open(file,'r',encoding='utf-8').read() or not all([(i in json.loads(open(file,'r',encoding='utf-8').read())) for i in init.party_space]):
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(graphee, f, ensure_ascii=False)

def plotter(array, color_array, label_array, html_path):
    with open(html_path, 'w', encoding='utf-8') as html:
        enum = enumerate(array[-1])
        charts = ht.groupGCharts([ht.createGChart('Pie', [['정당', '검색률']]+[[label_array[PARTY_NO], j] for PARTY_NO, j in enum], 'pie_chart', '정당 빅데이터'),
            ht.createGChart('Line', [["no"]+label_array]+[[NO]+j for NO, j in enumerate([(el/sum(el)*100).tolist() for el in array])], 'line_chart', '추이')])

        NEW_HTML = ht.Document(html_path, ht.basis, list(itertools.chain(*[charts['head'],
            [ht.Stylesheet('https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css', True,
                integrity='sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH',
                crossorigin='anonymous')],
            [ht.Script('https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js', True,
                integrity='sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz',
                crossorigin='anonymous')]])),
            list(itertools.chain(*[[ht.HTMLTag('div', id='chart_container', style='width: 100%; height: 1050px; background-color#eee').adopted(charts['body'])]]))).HTML
        
        html.write(NEW_HTML)

def dataGrabber(GRAPHEE, file, array, html_path):
    headers = json.loads(open('secrets.json', 'r').read())
    commonWord = "오늘"
    print('실행 시작')
    newFile(GRAPHEE, file)
    url = f'https://openapi.naver.com/v1/search/blog.json?query={commonWord}&sort=date'
    response = requests.get(url, headers=headers).json()
    GRAPHEE["기준"] = int(response["items"][0]["link"].split("/")[-1])
    for i in init.party_space:
        time.sleep(0.3)
        GRAPHEE[i].append([])
        if len(GRAPHEE[i])>10:
            del GRAPHEE[i][0]
        for j, KEYWORD in enumerate(init.party_space[i].keywords):
            print(KEYWORD)
            url = f'https://openapi.naver.com/v1/search/blog.json?query={KEYWORD}&start=100&sort=date'
            response = requests.get(url, headers=headers).json()
            if "items" not in response:
                GRAPHEE[i][-1].append(GRAPHEE[i][-2][j])
            GRAPHEE[i][-1].append(int(response["items"][0]["link"].split("/")[-1]))
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(GRAPHEE, f, ensure_ascii=False)
    calculated = calc.calculator(file)[:-1]
    print(calculated)
    array.append(calculated)
    if len(array)>60:
        del array[0]
    plotter(array, ['blue', 'red', 'yellow', 'orange', 'navy'], ['더불어민주당', '국민의힘', '녹색정의당', '개혁신당', '조국혁신당'], html_path)
