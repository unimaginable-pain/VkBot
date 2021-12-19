import requests
import json

class AutoFormatter:
    def __init__(self, func, text):
        if not callable(func):
            return "Error: expected callable function"
        self.f = func
        self.t = text
    def __call__(self, *args):
        r = self.f()
        return self.t.format(r)

class WebGetter:
    def __init__(self, url, is_json=True, json_levels=0, json_domains=None):
        self.target = url
        self.is_json = is_json
        self.json_levels = json_levels
        self.json_domains = json_domains
    def __call__(self, *args):
        res = requests.get(self.target).text
        if not self.is_json or self.json_levels < 1 or self.json_domains==None:
            return res
        j = json.loads(res)
        for i in range(self.json_levels):
            j = j[self.json_domains[i]]
        return j
        
