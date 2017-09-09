import json


def load_extracted_features():
    with open('data.json', 'r', encoding='utf8') as infile:
        temp_json = json.load(infile)
    with open('featuredata.json', 'w', encoding='utf8') as featuredata:
        writable_features = _extract_features(temp_json)
        json.dump(writable_features, featuredata, indent=4,
                  sort_keys=True, separators=(',', ': '), ensure_ascii=False)


def _extract_features(jsondata):
    temp = []
    feature_list = ['typeLine', 'explicitMods', 'ilvl', 'league', 'properties', 'sockets', 'corrupted', 'note']
    for stash in jsondata:
        for item in stash['items']:
            # to modify temp_dict separately have to do this temp_dict = dict(item)
            temp_dict = dict(item)
            for att in item:
                if att not in feature_list:
                    del temp_dict[att]
            for feature in feature_list:
                if feature not in temp_dict:
                    temp_dict[feature] = 0
            temp.append(temp_dict)
    return temp


def generate_training_test_sets():
    with open('training.json', 'w', encoding='utf8') as trainfile:
        json.dump([], trainfile)
    with open('featuredata.json', 'r', encoding='utf8') as infile:
        featuredata = json.load(infile)
    training_example = {}


load_extracted_features()
