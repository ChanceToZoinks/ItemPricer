import json
import os


class ItemPriceTrainingSetup:

    def load_extracted_features(self):
        with open('data.json', 'r', encoding='utf8') as infile:
            temp_json = json.load(infile)
        with open('featuredata.json', 'w', encoding='utf8') as featuredata:
            writable_features = self._extract_features(temp_json)
            json.dump(writable_features, featuredata, indent=4,
                      sort_keys=True, separators=(',', ': '), ensure_ascii=False)

    def _extract_features(self, jsondata):
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

    def generate_training_file(self):
        with open('training.json', 'r+', encoding='utf8') as trainfile:
            if os.stat('training.json').st_size == 0:
                json.dump([], trainfile)

        training_example = {'Armour': 0, 'Evasion Rating': 0, 'Energy Shield': 0, 'Life': 0, 'Mana': 0,
                            'Resistance': 0, 'Avg Phys Damage': 0, 'Avg Ele Damage': 0, 'Rarity': 0,
                            'Intelligence': 0, 'Strength': 0, 'Dexterity': 0, 'Attack Speed': 0, 'Local Crit Chance': 0,
                            'Global Crit Chance': 0, 'Crit Strike Multiplier': 0, 'Spell Damage': 0, 'Accuracy': 0,
                            'Ele Damage With Attacks': 0, 'Movement Speed': 0, 'Spell Crit Chance': 0, 'Cast Speed': 0,
                            'Sockets': 0, 'Links': 0, '+1 Gems': 0
                            }
        with open('training.json', 'r', encoding='utf8') as trainfile:
            training_file_data = json.load(trainfile)

        with open('training.json', 'w', encoding='utf8') as trainfile:
            training_file_data.append(training_example)
            json.dump(training_file_data, trainfile, indent=4,
                      sort_keys=True, separators=(',', ': '), ensure_ascii=False)


i = ItemPriceTrainingSetup()

i.load_extracted_features()
i.generate_training_file()
