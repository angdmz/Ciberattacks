import json
from unittest import TestCase


class DataExtractor(object):

    def string_accesses_array(self, string):
        i = len(string) -1
        string_accesses = False
        key = string
        number = 0
        if string[i] is ']':
            i -= 1
            while i >= 0 and string[i].isdigit():
                 number = number + int(string[i]) * (10 ** (len(string)-1 -i))
                 i-=1
            if string[i] is '[':
                string_accesses = True
                key = string[:i]

        return string_accesses, key, number

    def extract_recursion(self, content, target):
        if not type(content) is dict:
            return
        if len(target) is 1:
            string_accesses_array, key, position = self.string_accesses_array(target[0])
            value = content.get(key, None)
            if value is not None and type(value) is list and string_accesses_array:
                if len(value) > position:
                    return value[position]
                else:
                    return
            return value
        return self.extract_recursion(content.get(target[0],None), target[1:])

    def extract(self, content, target):
        d = json.loads(content)
        extracted = dict()
        for t in target:
            e = self.extract_recursion(d, t.split('.'))
            if e is not None:
                extracted[t] = e
        return extracted


class TestExtractor(TestCase):
    def setUp(self):
        self.data_extractor = DataExtractor()

    def test_simple_extraction(self):
        a = '{"guid": "1234","content": { "type": "text/html", "title": "Challenge 1", "entities": ["1.2.3.4", "wannacry", "malware.com"] }, "score": 74, "time": 1574879179 }'
        b = ["guid", "content.entities", "score", "score.sign"]
        data = self.data_extractor.extract(a,b)
        expected = { "guid": "1234", "content.entities": [ "1.2.3.4", "wannacry", "malware.com"], "score": 74}
        self.assertEqual(expected, data)

    def test_not_existing_simple_extraction(self):
        a = '{"guid": "1234","content": { "type": "text/html", "title": "Challenge 1", "entities": ["1.2.3.4", "wannacry", "malware.com"] }, "score": 74, "time": 1574879179 }'
        b = [ "score.sign"]
        data = self.data_extractor.extract(a,b)
        expected = {}
        self.assertEqual(expected, data)

    def test_nested_extraction(self):
        a = '{"guid": "1234","content": {"link": {"href": {"parent": "someValue"} }, "type": "text/html", "title": "Challenge 1", "entities": ["1.2.3.4", "wannacry", "malware.com"] }, "score": 74, "time": 1574879179 }'
        b = ["guid", "content.link.href.parent", "score", "score.sign"]
        data = self.data_extractor.extract(a, b)
        expected = {"guid": "1234", "content.link.href.parent": "someValue", "score": 74}
        self.assertEqual(expected, data)

    def test_nested_array_extraction(self):
        a = '{"guid": "1234","content": {"link": {"href": {"parent": ["v1","v2","v3"]} }, "type": "text/html", "title": "Challenge 1", "entities": ["1.2.3.4", "wannacry", "malware.com"] }, "score": 74, "time": 1574879179 }'
        b = ["guid", "content.link.href.parent", "score", "score.sign"]
        data = self.data_extractor.extract(a, b)
        expected = {"guid": "1234", "content.link.href.parent": ["v1","v2","v3"], "score": 74}
        self.assertEqual(expected, data)

    def test_array_extraction(self):
        a = '{"guid": "1234","content": { "type": "text/html", "title": "Challenge 1", "entities": ["1.2.3.4", "wannacry", "malware.com"] }, "score": 74, "time": 1574879179 }'
        b = ["content.entities[0]", ]
        data = self.data_extractor.extract(a,b)
        expected = { "content.entities[0]":  "1.2.3.4", }
        self.assertEqual(data, expected)

    def test_complete_array_extraction(self):
        a = '{"guid": "1234","content": { "type": "text/html", "title": "Challenge 1", "entities": ["1.2.3.4", "wannacry", "malware.com"] }, "score": 74, "time": 1574879179 }'
        b = ["guid", "content.entities[0]", "score", "score.sign"]
        data = self.data_extractor.extract(a,b)
        expected = { "guid": "1234", "content.entities[0]": "1.2.3.4" , "score": 74}
        self.assertEqual(data, expected)

    def test_complete_array_not_valid_extraction(self):
        a = '{"guid": "1234","content": { "type": "text/html", "title": "Challenge 1", "entities": ["1.2.3.4", "wannacry", "malware.com"] }, "score": 74, "time": 1574879179 }'
        b = ["guid", "content.entities[dfg0]", "score", "score.sign"]
        data = self.data_extractor.extract(a,b)
        expected = { "guid": "1234",  "score": 74}
        self.assertEqual(data, expected)

    def test_complete_array_another_not_valid_extraction(self):
        a = '{"guid": "1234","content": { "type": "text/html", "title": "Challenge 1", "entities": ["1.2.3.4", "wannacry", "malware.com"] }, "score": 74, "time": 1574879179 }'
        b = ["guid", "content.entities[345]", "score", "score.sign"]
        data = self.data_extractor.extract(a,b)
        expected = { "guid": "1234",  "score": 74}
        self.assertEqual(data, expected)

    def test_not_set_nested_extraction(self):
        a = '{"guid": "1234","content": {"link": {"nothref": {"parent": ["v1","v2","v3"]} }, "type": "text/html", "title": "Challenge 1", "entities": ["1.2.3.4", "wannacry", "malware.com"] }, "score": 74, "time": 1574879179 }'
        b = ["content.link.href.parent", ]
        data = self.data_extractor.extract(a, b)
        expected = {}
        self.assertEqual(data, expected)

    def test_not_set_nested_array_extraction(self):
        a = '{"content": {"type": "text/html", "title": "Challenge 1", "entities": [{"time":"00:00:00"} , "wannacry", "malware.com"] }, "score": 74, "time": 1574879179 }'
        b = ["content.entities[0].time", ]
        data = self.data_extractor.extract(a, b)
        expected = {'content.entities[0].time':"00:00:00"}
        self.assertEqual(data, expected)

    def test_not_set_nested_array_not_valid_extraction(self):
        a = '{"guid": "1234","content": {"link": {"nothref": {"parent": ["v1","v2","v3"]} }, "type": "text/html", "title": "Challenge 1", "entities": ["1.2.3.4", "wannacry", "malware.com"] }, "score": 74, "time": 1574879179 }'
        b = ["content.entities[0].time", ]
        data = self.data_extractor.extract(a, b)
        expected = {}
        self.assertEqual(data, expected)
