

class testCase:    
    def __init__(self, score1, score2, score_diff, testParam, sigTest, effSize, powAnaly):
        self.score1 = score1
        self.score2 = score2
        self.score_diff = score_diff
        self.testParam = testParam
        self.sigTest = sigTest
        self.effSize = effSize
        self.powAnaly = powAnaly


    def calc_score_diff(self):
        self.score_diff = {}
        for i in self.score1.keys():
            self.score_diff[i] = self.score1[i]-self.score2[i]