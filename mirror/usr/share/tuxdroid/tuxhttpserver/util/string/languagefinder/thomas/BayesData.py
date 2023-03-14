class BayesData(dict):

    def __init__(self, name='', pool=None):
        self.name = name
        self.training = []
        self.pool = pool
        self.tokenCount = 0
        self.trainCount = 0

    def trainedOn(self, item):
        return item in self.training

    def __repr__(self):
        return '<BayesDict: %s, %s tokens>' % (self.name, self.tokenCount)
