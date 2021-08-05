########################################################################
# Cric API Calls
########################################################################
import requests
import json

from models import MatchInfo

class CricAPI(object):
    def __init__(self, match_url):
        self.match_url = match_url

    def get_live_score(self):
        return MatchInfo(self._call_api(self._get_livescore_endpoint()))

    
    def _call_api(self, endpoint):
        s = requests.Session()
        res = s.get(endpoint)
        if res.status_code == requests.codes.ok:
            return json.loads(res.content.decode('utf-8'))
        else:
            raise res.raise_for_status()

    def _get_livescore_endpoint(self):
        return 'https://cricket-api.vercel.app/cri.php?url={cricbuzz_url}'\
            .format(cricbuzz_url=requests.utils.quote(self.match_url))