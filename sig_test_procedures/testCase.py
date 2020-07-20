"""
This is a script containing the object testCase class.
"""
class testCase:    
    def __init__(self, score1, score2, score_diff, sample_size, output_dir=''):
        # attributes
        self.score1 = score1
        self.score2 = score2
        self.score_diff = score_diff
        self.sample_size = sample_size
        self.output_dir = output_dir

        self.eda = self.eda(0, False, '', 1, False, '', None)

        self.sigTest = self.sigTest('', 0.05, 0, 0, 0, False)

        self.es = self.es([],[])

        self.power = self.power({},'',0.05, 5, 0.8)



    class eda:
        def __init__(self, m, isShuffled, calc_method, randomSeed, normal, testParam, testName):
            self.m = m
            self.isShuffled = isShuffled
            self.calc_method = calc_method
            self.randomSeed = randomSeed
            self.normal = normal
            self.testParam = testParam
            self.testName = testName

    class sigTest:
        def __init__(self, testName, alpha, mu, test_stat, pval, rejection):
            self.testName = testName
            self.alpha = alpha
            self.mu = mu
            self.test_stat = test_stat
            self.pval = pval
            self.rejection = rejection

    class es:
        def __init__(self, estimate, estimator):
            self.estimate = estimate
            self.estimator = estimator

    class power:
        def __init__(self, powerCurve, method, alpha, step_size, pow_lev):
            self.powerCurve = powerCurve
            self.method = method
            self.step_size = step_size
            self.pow_lev = pow_lev



    def calc_score_diff(self):
        self.score_diff = {}
        for i in self.score1.keys():
            self.score_diff[i] = self.score1[i]-self.score2[i]

