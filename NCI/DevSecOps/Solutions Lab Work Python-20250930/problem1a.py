class Greetings:
    
    def __init__(self, name):
        self.full_name = name
        
    # an example of an instance method
    def say_hi(self):
        return "Hello {}".format(self.full_name)
