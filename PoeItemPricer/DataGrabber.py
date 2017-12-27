from PoEApiTools import PoeApiTools as pat
import json
import os
from copy import deepcopy


def LoadFeatureTemplate():
    with open('example_template.json') as f:
        return json.load(f)


def CreateTrainingExample(itemDict, templateDict=LoadFeatureTemplate()):
    """This parses the given raw itemDict and returns it in a usable form based on a template"""
    # deepcopy because the item dicts will have other containers within them usually
    base = deepcopy(templateDict)

    base['id'] = itemDict['id']
    base['ilvl'] = itemDict['ilvl']

    if itemDict['league'].lower() in base:
        base[itemDict['league'].lower()] = 1
    elif 'Hardcore' in itemDict['league']:
        base['season HC'] = 1
    else:
        base['season'] = 1

    # parse properties field
    try:
        base[itemDict['properties'][0]['name'].lower()] = 1
        for i in itemDict['properties'][1:]:
            if i['name'].lower() in base:
                for x in i['values']:
                    # ele damage/phys have ranges seperated by -
                    if '-' in x[0]:
                        l, h = x[0].split('-')
                        base[i['name'].lower()] += float((int(l) + int(h)) / 2)
                    # crit chance is given as a %
                    elif '%' in x[0]:
                        base[i['name'].lower()] = float(x[0].replace('%', ''))
                    else:
                        base[i['name'].lower()] = float(x[0])
    except KeyError:
        pass

    # parse implicits
    try:
        for i in itemDict['implicitMods']:
            if i.lower() is 'critical strike chance':
                pass
            else:
                if "%" in x:
                    base[i] += float(x.split("%")[0].strip('+'))
                else:
                    base[i] += float(x.split(" ")[0].strip('+'))
        for i in base:
            y = [x.lower() for x in itemDict['implicitMods']]
            for w in y:
                if 'global critical strike chance' in w:
                    base['global critical strike chance'] = float(w.split("%")[0].strip('+'))
                elif i in w.lower() and 'critical strike chance' not in i:
                    if "%" in w:
                        base[i] += float(w.split("%")[0].strip('+'))
                    else:
                        base[i] += float(w.split(" ")[0].strip('+'))

    except KeyError:
        pass

    return base


def UpdateDatasetFile(trainingExample):
    try:
        with open('item_dataset.json', 'r+', encoding='utf8') as dataset_file:
            if os.stat('item_dataset.json').st_size == 0:
                json.dump([], dataset_file)
    except IOError:
        with open('item_dataset.json', 'w'):
            print('File not found, creating it.')
        with open('item_dataset.json', 'r+', encoding='utf8') as dataset_file:
            if os.stat('item_dataset.json').st_size == 0:
                json.dump([], dataset_file)

    # store the old json data
    with open('item_dataset.json', 'r', encoding='utf8') as dataset_file:
        training_file_data = json.load(dataset_file)

    # append new data to old and rewrite the file with the new data excluding any duplicates
    with open('item_dataset.json', 'w', encoding='utf8') as dataset_file:
        training_file_data_old = deepcopy(training_file_data)
        training_file_data.append(trainingExample)
        for i in training_file_data_old:
            if trainingExample['id'] in i['id']:
                json.dump(training_file_data_old, dataset_file, indent=4,
                          sort_keys=False, separators=(',', ': '), ensure_ascii=False)
                return
        json.dump(training_file_data, dataset_file, indent=4,
                  sort_keys=False, separators=(',', ': '), ensure_ascii=False)


t = pat.GGGGetPublicStashData(changeID='2524-4457-4108-4873-1427')
item1 = t['stashes'][20]['items'][9]
item2 = t['stashes'][34]['items'][7]
item3 = t['stashes'][71]['items'][9]
item4 = t['stashes'][71]['items'][6]
UpdateDatasetFile(CreateTrainingExample(item1))
UpdateDatasetFile(CreateTrainingExample(item2))
UpdateDatasetFile(CreateTrainingExample(item3))
UpdateDatasetFile(CreateTrainingExample(item4))

