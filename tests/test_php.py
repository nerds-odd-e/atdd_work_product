import unittest
from pyphp import phpApp, Persist

class FakePersist(object):
    def save(self, content): pass
    def load(self): return []

class PhpTestMixin(object):
    
    def initTestMixin(self):
        self.saved_contents_ = []
        self.saved_write_line = phpApp.write_line
        phpApp.write_line = lambda s, x:self.saved_contents_.append(x)

    def teardown(self):
        phpApp.write_line = self.saved_write_line

    def clearSavedOutput(self):
        self.saved_contents_ = []
        
class TestPhp(unittest.TestCase, PhpTestMixin):
    
    def setUp(self):
        self.initTestMixin()
        self.app = phpApp(FakePersist())

    def test_should_say_hello_when_no_command(self):
        self.app.main([])
        self.assertIn("Hello from PHP!", self.saved_contents_)
        
    def test_should_say_unknown_command(self):
        self.app.main(['unknown'])
        self.assertIn("Command 'unknown' is unknown.", self.saved_contents_)
        
    def test_should_say_not_found_when_retrieve_nonexisting_record(self):
        self.app.main(['retrieve', 'NONEXISTING_RECORD'])
        self.assertIn('Record Not Found.', self.saved_contents_)
        
    def test_should_get_record_when_retrieve_existing_record(self):
        self.app.main(['retrieve', 'EXISTING_RECORD'])
        self.assertIn('EXISTING_RECORD', self.saved_contents_)

    def test_should_say_successful_after_creating_record(self):
        self.app.main(['create', 'NEW_RECORD'])
        self.assertIn('Successful.', self.saved_contents_)

    def test_should_be_able_to_retrieve_record_after_creating_record(self):
        self.app.main(['create', 'NEW_RECORD'])
        self.clearSavedOutput()
        self.app.main(['retrieve', 'NEW_RECORD'])
        self.assertIn('NEW_RECORD', self.saved_contents_)

class TestPersistant(unittest.TestCase, PhpTestMixin):

    def setUp(self):
        self.initTestMixin()

    def test_should_be_able_to_retrieve_persistent_record(self):
        phpApp(Persist()).main(['create', 'PERSIST_RECORD'])
        self.clearSavedOutput()
        phpApp(Persist()).main(['retrieve', 'PERSIST_RECORD'])
        self.assertIn('PERSIST_RECORD', self.saved_contents_)

    def test_should_return_empty_record_when_file_is_corrupted(self):
        persist = Persist()
        persist.FILE_NAME = 'corupted_file'
        phpApp(persist).main(['retrieve', 'PERSIST_RECORD'])
        self.assertIn('Record Not Found.', self.saved_contents_)

class TestAttributes(unittest.TestCase, PhpTestMixin):

    def setUp(self):
        self.initTestMixin()
        self.app = phpApp(FakePersist())
    
    def xtest_create_and_get_new_attribute(self):
        self.app.main(['create', 'NEW_RECORD'])
        self.clearSavedOutput()
        self.app.main(['attribute', 'first name', 'john'])
        self.app.main(['retrieve', 'NEW_RECORD'])
        self.assertIn('NEW_RECORD', self.saved_contents_)
        self.assertIn('[first name] john', self.saved_contents_)
        



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()