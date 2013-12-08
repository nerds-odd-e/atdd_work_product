import pickle

class PhpDirectory(object):

    def __init__(self, content):
        self.records = content

    def retrieve(self, record_name):
        return self.records.get(record_name, None)

    def create(self, record_name):
        self.records[record_name] = {}
        
    def attribute(self, record_name, attribute_name, attribute_value):
        self.records[record_name][attribute_name] = attribute_value
    
    def format(self):
        self.records = {}

class phpApp(object):
    
    def __init__(self, persist):
        self.persist = persist
        self.directory = PhpDirectory(self.persist.load())
        
    def retrieve(self, record_name):
        record = self.directory.retrieve(record_name)
        if record is not None:
            self.write_line(record_name)
            for k, v in record.items():
                self.write_line('[%s] %s' % (k, v))
        else:
            self.write_line("Record Not Found.")

    def create(self, record_name):
        if self.directory.retrieve(record_name) is not None:
            self.write_line("Duplicate Record and Failed to create.")
            return
        
        self.directory.create(record_name)
        self.write_line("Successful.")

    def attribute(self, record_name, attribute_name, attribute_value):
        self.directory.attribute(record_name, attribute_name, attribute_value)
        self.write_line("Successful.")
    
    def format(self):
        self.directory.format()
        self.write_line("All Data Erased.")
    
    def unknown(self, *v):
        self.write_line("Command is unknown.")
        
    def main(self, argv):
        if len(argv) == 0:
            self.write_line('Hello from PHP!')
            return
        
        getattr(self, argv[0], self.unknown)(*argv[1:])
        self.persist.save(self.directory.records)

    def write_line(self, content):
        print content

class Persist(object):
    
    FILE_NAME = 'php.pickle'
    
    def save(self, content):
        with open(self.FILE_NAME, 'w') as file:
            pickle.dump(content, file)

    def load(self):
        try:
            with open(self.FILE_NAME, 'r') as file:
                return pickle.load(file)
        except IOError:
            return {}
        
def main():
    import sys
    phpApp(Persist()).main(sys.argv[1:])

if __name__ == '__main__':
    main()