class Dog:
    def bark(self):
        print('haf-haf')


class Cat:
    def mew(self):
        print('myau-myau')


class Anasun(Dog, Cat):
    pass


ez = Anasun()
ez.bark()
ez.mew()