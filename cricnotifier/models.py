########################################################################
# Models according to Cric API
########################################################################

class MatchInfo(object):
    def __init__(self, matchdata):
        self.data = matchdata if matchdata else {}

    @property
    def last_wicket(self):
        if self.data['livescore'] and '-' in self.data['livescore']['lastwicket']:
            return self.data['livescore']['lastwicket']
        
        return ''
