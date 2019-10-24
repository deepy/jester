import sys
import xml.etree.ElementTree as ET


def extract_testdata(path):
    root = ET.parse(path).getroot()
    test = root.attrib.copy()
    test['testcases'] = []
    for child in root:
        if child.tag == 'system-out' and child.text:
            test['stdout'] = child.text
        elif child.tag == 'system-err' and child.text:
            test['stderr'] = child.text
        elif child.tag == 'properties':
            properties = {}
            for prop in child:
                if prop.tag == 'property':
                    key = prop.attrib['name']
                    value = prop.attrib['value']
                    if key is not None and value is not None:
                        properties[key] = value
            if properties:
                test['properties'] = properties
        elif child.tag == 'testcase':
            result = child.attrib.copy()
            result['result'] = 'success'
            # print(child.tag, child.text, child.attrib)
            for entry in child:
                # Should probably not do this, but getting the last result seems fine.
                result['result'] = entry.tag
                if entry.attrib.get('message'):
                    result['message'] = entry.attrib['message']
            test['testcases'].append(result)

        # print(child.tag)
    return test


def launch():
    result = extract_testdata(sys.argv[2])
    try:
        import pprint
        pprint.pprint(result)
    except ImportError:
        print(result)
    if sys.argv[1] == 'post':
        import requests
        result['source'] = [kv('Gradle Task', 'systemAcceptanceTest')]
        r = requests.post('http://localhost:5000/post', json=result)
        print(r.text)


def kv(key, value):
    return {'name': key, 'value': value}


if __name__ == '__main__':
    launch()
