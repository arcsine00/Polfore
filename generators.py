from classes.documentTypeClasses import *
from classes.processorClasses import *
import numpy as np

parties = [[], ['민주당'], ['국민의힘', '국힘', '국힘당'], [], [], ['정의당'], [], ['개혁신당'], ['조국혁신당']]
NUM_OF_PARTIES = len(parties)
party_space = {}

class Party:
    def __init__(self, num):
        self.candidate_number = num
        self.name = parties[num][0]
        self._base = ' | '.join(parties[num])
        self._EXCEPT = ' '.join([f'-{i}' for i in sum(parties[:num]+(parties[-len(parties)+num+1:])*(not not -len(parties)+num+1), [])])
        self.keywords = [self._base, f'{self._base} 지지', f'{self._base} 후보', f'{self._base} 선거']

for i in range(NUM_OF_PARTIES):
    if parties[i]:
        party_space[parties[i][0]] = Party(i)

print([party_space[i].keywords for i in party_space])

class ChartBox:
    def __init__(self, name: str, keyword_arr: list[list[str]], max_grabs: int, raw_data_output: str):
        self.name = name
        self.groups_of_grabbers = []
        self.labels = []
        self.keyword_arr = keyword_arr
        self.max_grabs = max_grabs

        for big_category in self.keyword_arr:
            self.groups_of_grabbers.append([])
            self.labels.append(big_category[0].split(' ')[0])
            for keyword in big_category:
                self.groups_of_grabbers[-1].append(JSONDataGrabber(keyword, ['items'], ['items', 'link'], self.max_grabs))
            self.groups_of_grabbers[-1] = JSONGrabberGroup(self.groups_of_grabbers[-1], 0)
        self.raw_data_output = raw_data_output
        self._updater = JSONUpdater(self.raw_data_output, self.groups_of_grabbers)

    def __call__(self):
        self._updater()
        return self

    def processedAt(self, processed_data_output: str, constants: list[float]):
        self.processed_data_output = processed_data_output
        self._mixer = DataMixer(self.raw_data_output, self.processed_data_output)
        self._mixer(constants)
        return self

    def renderedInto(self, color_array: list[str]):
        with open(self.processed_data_output, 'r', encoding='utf-8') as js:
            data = np.array(list(json.loads(js.read()).values())).T.tolist()
            return ChartDocument(self.name, [PieChart(data, color_array, self.labels, self.name), LineChart(data, color_array, self.labels, '추이')])

def initChartBox(title: str, space: dict[str, Party]):
    chartbox = ChartBox(title, [space[i].keywords for i in space], 60, f'lib/{title}_raw.json')
    return chartbox

def updateChartBox(chartbox: ChartBox, weight: list[float]):
    doc = chartbox().processedAt(f'lib/{chartbox.name}_weight_{"_".join([str(int(i*100)) for i in weight])}.json', weight).renderedInto([])
    with open(doc.name, 'w', encoding='utf-8') as html:
        html.write(doc.HTML)
