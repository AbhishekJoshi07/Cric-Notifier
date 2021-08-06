########################################################################
# Models according to Cric API
########################################################################

DATA_NOT_FOUND = 'Data Not Found'

class MatchInfo(object):
    def __init__(self, matchdata):
        self.data = matchdata if matchdata else {}

    @property
    def last_wicket(self):
        if self.data['livescore'] and '-' in self.data['livescore']['lastwicket']:
            return self.data['livescore']['lastwicket']
        
        return ''

    @property
    def live_score(self):
        if self.data['livescore'] and '(' in self.data['livescore']['current']:
            return self.data['livescore']['current']
        
        return ''

    @property
    def current_runrate(self):
        if self.data['livescore'] and ':' in self.data['livescore']['runrate']:
            return self.data['livescore']['runrate']
        
        return ''

    @property
    def batsman(self):
        if self.data['livescore'] and self.data['livescore']['batsman'] != DATA_NOT_FOUND:
            return self.data['livescore']['batsman']
        
        return ''

    @property
    def batsmanrun(self):
        if self.data['livescore'] and self.data['livescore']['batsmanrun'].isnumeric():
            return int(self.data['livescore']['batsmanrun'])
        
        return 0

    @property
    def batsman_ballsfaced(self):
        if self.data['livescore'] and '(' in self.data['livescore']['ballsfaced']:
            return self.data['livescore']['ballsfaced']
        
        return ''

    @property
    def batsaman_fours(self):
        if self.data['livescore'] and self.data['livescore']['fours'] != DATA_NOT_FOUND:
            return self.data['livescore']['fours']
        
        return ''

    @property
    def batsaman_sixes(self):
        if self.data['livescore'] and self.data['livescore']['sixes'] != DATA_NOT_FOUND:
            return self.data['livescore']['sixes']
        
        return ''

    @property
    def partnership(self):
        if self.data['livescore'] and '(' in self.data['livescore']['partnership']:
            return self.data['livescore']['partnership']
        
        return ''

    @property
    def recentballs(self):
        if self.data['livescore'] and '|' in self.data['livescore']['recentballs']:
            return self.data['livescore']['recentballs']
        
        return ''

    @property
    def bowler(self):
        if self.data['livescore'] and self.data['livescore']['bowler'] != DATA_NOT_FOUND:
            return self.data['livescore']['bowler']
        
        return ''

    @property
    def bowlerwickets(self):
        if self.data['livescore'] and self.data['livescore']['bowlerwickets'].isnumeric():
            return int(self.data['livescore']['bowlerwickets'])
        
        return 0
