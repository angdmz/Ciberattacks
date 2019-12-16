import json


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

    def extract(self, content, target):
        d = json.loads(content)
        extracted = dict()
        for t in target:
            splitted = t.split('.')
            c = d
            i = 0
            while c is not None and len(splitted) > i:
                s = splitted[i]
                string_accesses_array, key, position = self.string_accesses_array(s)
                if string_accesses_array and type(c.get(key ,None)) is list and len(c[key]) > position:
                    c = c[key][position]
                elif type(c) is dict:
                    c = c.get(s, None)
                else:
                    c = None
                i += 1

            if c is not None:
                extracted[t] = c
        return extracted