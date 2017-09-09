import requests
import json


class StashGrabber:
    temp_stash_json = []

    def parse_stash_json(self, stash_json):
        for stash in stash_json['stashes']:
            if stash['public']:
                if len(stash['items']) > 0:
                    for i in list(stash.keys()):
                        if i != 'stash' and i != 'items':
                            del stash[i]
                    temp_stash = stash
                    self._keep_only_rares(temp_stash)
                    self.temp_stash_json.append(temp_stash)
        JsonWriter.write_json(self.temp_stash_json)

    def _keep_only_rares(self, temp_stash):
        for item in range(len(temp_stash['items'])-1, -1, -1):
            if temp_stash['items'][item]['frameType'] != 2:
                print(item)
                del temp_stash['items'][item]


class StashAPIRequester:
    stash_URL = 'http://www.pathofexile.com/api/public-stash-tabs'
    change_id_url = 'http://api.poe.ninja/api/Data/GetStats'
    n = requests.get(change_id_url)

    next_change_id = n.json()['nextChangeId']
    params = {'id': next_change_id}

    j = StashGrabber()

    r = 0
    r_json = 0

    def get_next_change(self):
        self.r = requests.get(self.stash_URL, params=self.params)
        self.r_json = self.r.json()
        self.j.parse_stash_json(self.r_json)
        print(self.next_change_id)


class JsonWriter:
    @staticmethod
    def write_json(parsed_json):
        with open('data.json', 'w', encoding='utf8') as outfile:
            json.dump(parsed_json, outfile, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)


s = StashAPIRequester()

s.get_next_change()
