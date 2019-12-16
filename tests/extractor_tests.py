from unittest import TestCase

from extraction.extractor import DataExtractor


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

    def test_escaped_characters_prod_config(self):
        a = '{ "type": "bundle", "id": "bundle--bf3c8e50-62a0-440f-9936-279bf4ad34bb", "spec_version": "2.0", "objects": [ { "x_mitre_data_sources": [ "Process use of network", "Process monitoring", "Process command-line parameters", "Anti-virus", "Binary file metadata" ], "kill_chain_phases": [ { "kill_chain_name": "mitre-attack", "phase_name": "defense-evasion" } ], "name": "Indicator Removal from Tools", "description": "If a malicious tool is detected and quarantined or otherwise curtailed, an adversary may be able to determine why the malicious tool was detected (the indicator), modify the tool by removing the indicator, and use the updated version that is no longer detected by the target\'s defensive systems or subsequent targets that may use similar systems.\\n\\nA good example of this is when malware is detected with a file signature and quarantined by anti-virus software. An adversary who can determine that the malware was quarantined because of its file signature may use [Software Packing](https://attack.mitre.org/techniques/T1045) or otherwise modify the file so it has a different signature, and then re-use the malware.", "id": "attack-pattern--00d0b012-8a03-410e-95de-5826bf542de6", "x_mitre_platforms": [ "Linux", "macOS", "Windows" ], "object_marking_refs": [ "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168" ], "x_mitre_version": "1.0", "type": "attack-pattern", "x_mitre_detection": "The first detection of a malicious tool may trigger an anti-virus or other security tool alert. Similar events may also occur at the boundary through network IDS, email scanning appliance, etc. The initial detection should be treated as an indication of a potentially more invasive intrusion. The alerting system should be thoroughly investigated beyond that initial alert for activity that was not detected. Adversaries may continue with an operation, assuming that individual events like an anti-virus detect will not be investigated or that an analyst will not be able to conclusively link that event to other activity occurring on the network.", "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5", "created": "2017-05-31T21:30:54.176Z", "modified": "2018-10-17T00:14:20.652Z", "external_references": [ { "external_id": "T1066", "source_name": "mitre-attack", "url": "https://attack.mitre.org/techniques/T1066" } ], "x_mitre_defense_bypassed": [ "Log analysis", "Host intrusion prevention systems", "Anti-virus" ] } ] }'
        b = ["id", "objects[0].name", "objects[0].kill_chain_phases"]
        data = self.data_extractor.extract(a, b)
        expected = {"id": "bundle--bf3c8e50-62a0-440f-9936-279bf4ad34bb", "objects[0].name": "Indicator Removal from Tools", "objects[0].kill_chain_phases": [{"kill_chain_name": "mitre-attack","phase_name": "defense-evasion"}]}
        self.assertEqual(data, expected)
