########################################################################
# Models according to Cric API
########################################################################

DATA_NOT_FOUND = 'Data Not Found'
VALID_UPDATES_WORDS = ['start', 'break', 'rain', 'stop', 'stumps', 'lunch', 'toss', 'dinner', 'tea', 'win', 'won', 'loss', 'opt', 'choose', 'drawn']

class MatchInfo(object):
    def __init__(self, matchdata):
        self.data = { 'livescore': {} }
        if matchdata and 'livescore' in matchdata:
            self.data = matchdata

    @property
    def last_wicket(self):
        if 'lastwicket' in self.data['livescore'] and '-' in self.data['livescore']['lastwicket']:
            return self.data['livescore']['lastwicket']
        
        return ''

    @property
    def live_score(self):
        if 'current' in self.data['livescore'] and '(' in self.data['livescore']['current']:
            return self.data['livescore']['current']
        
        return ''

    @property
    def current_runrate(self):
        if 'runrate' in self.data['livescore'] and ':' in self.data['livescore']['runrate']:
            return self.data['livescore']['runrate']
        
        return ''

    @property
    def batsman(self):
        if 'batsman' in  self.data['livescore'] and self.data['livescore']['batsman'] != DATA_NOT_FOUND:
            return self.data['livescore']['batsman']
        
        return ''

    @property
    def batsmanrun(self):
        if 'batsmanrun' in self.data['livescore'] and self.data['livescore']['batsmanrun'].isnumeric():
            return int(self.data['livescore']['batsmanrun'])
        
        return 0

    @property
    def batsman_ballsfaced(self):
        if 'ballsfaced' in self.data['livescore'] and '(' in self.data['livescore']['ballsfaced']:
            return self.data['livescore']['ballsfaced']
        
        return ''

    @property
    def batsaman_fours(self):
        if 'fours' in self.data['livescore'] and self.data['livescore']['fours'] != DATA_NOT_FOUND:
            return self.data['livescore']['fours']
        
        return ''

    @property
    def batsaman_sixes(self):
        if 'sixes' in self.data['livescore'] and self.data['livescore']['sixes'] != DATA_NOT_FOUND:
            return self.data['livescore']['sixes']
        
        return ''

    @property
    def partnership(self):
        if 'partnership' in self.data['livescore'] and '(' in self.data['livescore']['partnership']:
            return self.data['livescore']['partnership']
        
        return ''

    @property
    def recentballs(self):
        if 'recentballs' in self.data['livescore'] and '|' in self.data['livescore']['recentballs']:
            return self.data['livescore']['recentballs']

        elif 'lastwicket' in self.data['livescore'] and '|' in self.data['livescore']['lastwicket']:
            return self.data['livescore']['lastwicket']
        
        return ''

    @property
    def bowler(self):
        if 'bowler' in self.data['livescore'] and self.data['livescore']['bowler'] != DATA_NOT_FOUND:
            return self.data['livescore']['bowler']
        
        return ''

    @property
    def bowlerwickets(self):
        if 'bowlerwickets' in self.data['livescore'] and self.data['livescore']['bowlerwickets'].isnumeric():
            return int(self.data['livescore']['bowlerwickets'])
        
        return 0

    @property
    def match_update(self):
        if 'update' in self.data['livescore']:
            for i in range(len(VALID_UPDATES_WORDS)):
                if VALID_UPDATES_WORDS[i] in self.data['livescore']['update'].lower():                    
                    return self.data['livescore']['update']
        
        return ''
