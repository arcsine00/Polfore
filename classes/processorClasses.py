import requests
import json
import time
import numpy as np
import os

class JSONResponse:
    def __init__(self, url: str, headers: dict, required_keys: list[str], target_int: list[str]):
        self.createdAt = time.time()
        self.url = url
        self.response = requests.get(self.url, headers=headers).json()
        self.key_existence = all([(key in self.response) for key in required_keys])
        self.int_validity = False
        if self.key_existence:
            self.target = self.response[f'{target_int[0]}'][0][f'{target_int[1]}'].split("/")[-1]
            if str(self.target).isdigit():
                self.int_validity = True

class JSONDataGrabber: #1-1 with a keyword
    def __init__(self, keyword: str, required_keys: list[str], target_int: list[str], max_grabs: int):
        self.headers = json.loads(open('secrets.json', 'r').read())
        self.keyword = keyword
        self.req_keys = required_keys
        self.target_addr = target_int

        self.criteria_url = f'https://openapi.naver.com/v1/search/blog.json?query=오늘&sort=date'
        self.url = f'https://openapi.naver.com/v1/search/blog.json?query={keyword}&start=100&sort=date'
        self.res = []
        self.max_grabs = max_grabs
        self.grabbed_data = []

    def __call__(self):
        self.criteria_res = JSONResponse(self.criteria_url, self.headers, self.req_keys, self.target_addr)
        self.res.append(JSONResponse(self.url, self.headers, self.req_keys, self.target_addr))
        if self.res[-1].int_validity and self.criteria_res.int_validity:
            self.grabbed_data.append([self.res[-1].createdAt, 100000/(abs(int(self.criteria_res.target)-int(self.res[-1].target)))])
        else:
            self.grabbed_data.append([self.res[-1].createdAt, 0])
        print(f'a JSONDataGrabber for keyword <{self.keyword}> has {len(self.res)} JSONResponse(s) and {len(self.grabbed_data)} grabbed data(s).')
        if len(self.grabbed_data) > self.max_grabs:
            print(f'<{self.keyword}>: Exceeded grabs: Removing the first data...')
            del self.grabbed_data[0]
            del self.res[0]
        return self

class JSONGrabberGroup: #1-1 with a group of keywords (e.g. a candidate, a party, ...)
    def __init__(self, grabbers: list[JSONDataGrabber], leader_loc: int):
        self.child_grabbers = grabbers
        self.name = grabbers[leader_loc].keyword
    def __call__(self):
        self.child_grabbers = [grabber() for grabber in self.child_grabbers]
        return self

class JSONUpdater:
    def __init__(self, fname: str, groups: list[JSONGrabberGroup]):
        self.filename = fname
        self.groups = groups
    def __call__(self):
        self.groups = [group() for group in self.groups]
        self.keys = [group.name for group in self.groups]
        self.values = [[grabber.grabbed_data for grabber in group.child_grabbers] for group in self.groups]
        with open(self.filename, 'r', encoding='utf-8') as f:
            self.old_content = json.loads(f.read())
        self.new_content = {}
        for key, value in zip(self.keys, self.values):
            self.new_content[key] = value
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.new_content, f, ensure_ascii=False) #Structure: {partyname: Keywords[[Timestamp,Data]]}

class DataMixer:
    def __init__(self, input_json: str, output_json: str):
        self.filename = input_json
        self.out_file = output_json
        self.output = {}
        with open(self.filename, 'r', encoding='utf-8') as f:
            self.input = json.loads(f.read())
            self.constants = np.ones(len(list(self.input.values())[0]))
    def __call__(self, constants: list[float]):
        if len(constants) == len(self.constants):
            self.constants = np.array(constants)
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.input = json.loads(f.read())
            for key in self.input.keys():
                self.output[key] = np.zeros(len(self.input[key][0]))
                for no, constant in enumerate(self.constants):
                    self.output[key] += np.array(self.input[key][no]).T[1]*constant
                self.output[key] = self.output[key].tolist()
            with open(self.out_file, 'w', encoding='utf-8') as f:
                json.dump(self.output, f, ensure_ascii=False)
