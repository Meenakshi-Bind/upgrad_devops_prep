class Greetings:
    
    full_name = ""
    
    # an example of a class method
    @classmethod   
    def say_hi(cls, name):
        cls.full_name = name
        return "Hello {}".format(cls.full_name)
