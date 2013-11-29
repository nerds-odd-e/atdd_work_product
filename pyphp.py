import pickle

class PhpDirectory(object):

    def __init__(self, content):
        self.records = content
        self.records.append('EXISTING_RECORD')

    def retrieve_record(self, record_name):
        if record_name in self.records:
            return record_name

    def create(self, record_name):
        self.records.append(record_name)

class phpApp(object):
    
    def __init__(self, persist):
        self.persist = persist
        self.directory = PhpDirectory(self.persist.load())
        self.records = self.persist.load()
        self.records.append('EXISTING_RECORD')
        
    def retrieve_record(self, record_name):
        if self.directory.retrieve_record(record_name):
            self.write_line(record_name)
        else:
            self.write_line("Record Not Found.")

    def create(self, record_name):
        self.directory.create(record_name)
        self.persist.save(self.directory.records)
        self.write_line("Successful.")

    def main(self, argv):
        if len(argv) == 0:
            self.write_line('Hello from PHP!')
            return
        
        command = argv[0]
        if command == 'create':
            record_name = argv[1]
            self.create(record_name)
        
        elif command == 'retrieve':
            record_name = argv[1]
            self.retrieve_record(record_name)
            
        else:
            self.write_line("Command '%s' is unknown." % command)
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
            return []
        
def main():
    import sys
    phpApp(Persist()).main(sys.argv[1:])

if __name__ == '__main__':
    main()