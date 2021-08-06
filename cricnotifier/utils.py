########################################################################
# Utils functions
########################################################################

def string_formater(str):
    if str:
        str = ''.join(str.split('\\'))
        return ''.join(str.split('*'))
    return ''

def century_calculator(runs):
    if not runs:
        return ''
        
    if runs >= 50 and runs < 100:
        return 'Half Century'
    elif runs >= 100 and runs < 200:
        return 'Century'
    elif runs >= 200 and runs < 300:
        return 'Double Century'
    elif runs >= 300 and runs < 400:
        return 'Triple Century'
    elif runs >= 400 and runs < 500:
        return 'Quadruple Century'
    
    return ''

########################################################################
# DB helper classes (mainly to faciliate serveress)
########################################################################

class SimpleKVDB(object):
    def __init__(self, db):
        self._db = db

    def __contains__(self, key):
        return key in self._db

    def __getitem__(self, key):
        return self._db[key]

    def __setitem__(self, key, value):
        self._db[key] = value
        self._db.sync()
