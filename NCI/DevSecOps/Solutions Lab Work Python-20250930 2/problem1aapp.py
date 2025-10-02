from problem1a import Greetings

a_name = input("enter your name: ")

my_obj_variable = Greetings(a_name)

greeting_message = my_obj_variable.say_hi()
print(greeting_message)

print(my_obj_variable.say_hi())
