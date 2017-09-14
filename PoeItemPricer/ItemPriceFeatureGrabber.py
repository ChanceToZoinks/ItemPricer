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
                        temp_dict[feature] = str(0)
                temp.append(temp_dict)
        return temp

    training_example = {'Armour': 0, 'Evasion Rating': 0, 'Energy Shield': 0, 'Life': 0, 'Mana': 0,
                        'Resistance': 0, 'Avg Phys Damage': 0, 'Avg Ele Damage': 0, 'Rarity': 0,
                        'Intelligence': 0, 'Strength': 0, 'Dexterity': 0, 'Local Attack Speed': 0, 'Local Crit Chance': 0,
                        'Global Crit Chance': 0, 'Crit Strike Multiplier': 0, 'Spell Damage': 0, 'Accuracy': 0,
                        'Ele Damage With Attacks': 0, 'Movement Speed': 0, 'Spell Crit Chance': 0, 'Attack Speed': 0,
                        'Cast Speed': 0, 'Sockets': 0, 'Links': 0, '+1 Gems': 0
                        }

    def _generate_training_file(self):
        with open('training.json', 'r+', encoding='utf8') as trainfile:
            if os.stat('training.json').st_size == 0:
                json.dump([], trainfile)

        with open('training.json', 'r', encoding='utf8') as trainfile:
            training_file_data = json.load(trainfile)

        with open('training.json', 'w', encoding='utf8') as trainfile:
            training_file_data.append(self.training_example)
            json.dump(training_file_data, trainfile, indent=4,
                      sort_keys=True, separators=(',', ': '), ensure_ascii=False)

    def main(self):
        # this method generates each training example and writes each one to the file
        # make sure to reset training_example each time
        with open('featuredata.json', 'r', encoding='utf8') as file:
            file_json = json.load(file)
        for item in file_json:
            print(item)
            self._extract_item_properties(item)
            self._generate_training_file()
            self._reset_training_example()

    def _reset_training_example(self):
        for x in self.training_example:
            self.training_example[x] = str(0)

    def _extract_item_properties(self, item_dict):
        # fills training_example's armor/eva/es values
        for x in item_dict['properties']:
            if isinstance(x, str):
                continue
            if 'Energy Shield' in x['name']:
                self.training_example['Energy Shield'] = int(x['values'][0][0])
            if 'Armour' in x['name']:
                self.training_example['Armour'] = int(x['values'][0][0])
            if 'Evasion Rating' in x['name']:
                self.training_example['Evasion Rating'] = int(x['values'][0][0])
            if 'Physical Damage' in x['name']:
                p = x['values'][0][0]
                l, h = p.split('-')
                self.training_example['Physical Damage'] = float((int(l) + int(h)) / 2)
            if 'Critical Strike Chance' in x['name']:
                self.training_example['Local Crit Chance'] = float(x['values'][0][0].replace('%', ''))
            if 'Attacks per Second' in x['name']:
                self.training_example['Local Attack Speed'] = float(x['values'][0][0])
            if 'Elemental Damage' in x['name']:
                f = x['values'][0][0]
                fl, fh = f.split('-')
                cl, ch, ll, lh = 0, 0, 0, 0
                if len(x['values']) == 2:
                    c = x['values'][1][0]
                    cl, ch = c.split('-')
                elif len(x['values']) == 3:
                    c = x['values'][1][0]
                    cl, ch = c.split('-')
                    l = x['values'][2][0]
                    ll, lh = l.split('-')
                self.training_example['Avg Ele Damage'] = float(((int(fl) + int(fh)) / 2) + (int(cl) + int(ch) / 2)
                                                                + (int(ll) + int(lh)) / 2)

    def _extract_item_explicit_mods(self, item_dict):
        for x in item_dict['explicitMods']:
            if isinstance(x, str):
                continue



i = ItemPriceTrainingSetup()

i.load_extracted_features()
i.main()
