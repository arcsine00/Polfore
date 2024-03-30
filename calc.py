import json
import numpy as np

def calculator(file):
    ratio = [0.25, 0.25, 0.25, 0.25]
    with open(file, 'r', encoding='utf-8') as f:
        js = json.load(f)
        CALC = np.zeros(len(js.keys()))
        for partyOrd, i in enumerate(list(js.keys())[:-1]):
            for k in range(len(js[i])):
                for num, j in enumerate(np.array(js[i][k])):
                    CALC[partyOrd] += float(100000/(abs(js["기준"]-j)+1))*ratio[num]
        return CALC
