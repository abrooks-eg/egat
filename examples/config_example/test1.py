from egat.testset import UnorderedTestSet

class Test1(UnorderedTestSet):
    def testStep1(self):
        # We can access the configuration parameters from inside any test function.
        base_url = self.configuration["base_url"]
        port = self.configuration["port"]
    def testStep2(self):
        pass
    def testStep3(self):
        pass
