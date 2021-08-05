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
