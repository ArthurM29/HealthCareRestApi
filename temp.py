class Dog:
    @classmethod
    def say_my_name(cls):
        print("I am a {}".format(cls.__name__))


class Puppy(Dog):
    pass
#
#
# class Anasun(Dog, Cat):
#     pass
#
#
# ez = Anasun()
# ez.bark()
# ez.mew()r


dog = Dog()
dog.say_my_name()

puppy = Puppy()
Puppy.say_my_name()